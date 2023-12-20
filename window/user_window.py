import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, \
    QListWidget, QListWidgetItem, QInputDialog
from PyQt5.QtCore import Qt, QTimer
from sqlalchemy import create_engine, Column, String, Integer, Enum, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from bd.connect import session, Lot, User, Bid


class UserWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()
        self.timers = {}
        self.last_bidders = {}  # Добавлен словарь для хранения последних ставок

    def init_ui(self):
        self.setWindowTitle(f'Добро пожаловать, {self.username}')
        self.setGeometry(200, 200, 800, 400)

        layout = QVBoxLayout()

        self.lot_list_label = QLabel('Список лотов:')
        self.lot_list = QListWidget(self)

        layout.addWidget(self.lot_list_label)
        layout.addWidget(self.lot_list)

        self.load_lots()

        self.lot_list.itemDoubleClicked.connect(self.place_bid)

        self.setLayout(layout)

    def load_lots(self):
        lots = session.query(Lot).all()
        for lot in lots:
            item = QListWidgetItem(
                f"{lot.name}: {lot.description}, Минимальная цена: {lot.min_price}, Текущая цена: {lot.current_price}, "
                f"Таймер: {lot.timer_seconds} сек")
            item.setData(Qt.UserRole, lot.id)
            self.lot_list.addItem(item)

    def place_bid(self, item):
        lot_id = item.data(Qt.UserRole)
        lot = session.query(Lot).filter_by(id=lot_id).first()

        if not lot.is_active():
            QMessageBox.warning(self, 'Лот закрыт', 'Этот лот больше не принимает ставки.')
            return

        bid_amount, ok = QInputDialog.getDouble(self, 'Ставка', 'Введите сумму ставки:')

        if ok:
            if bid_amount >= lot.min_price:
                lot.current_price = bid_amount
                user_id = session.query(User).filter_by(username=self.username).first().id

                # Обновляем словарь last_bidders
                self.last_bidders[lot_id] = {'user_id': user_id, 'amount': bid_amount}

                new_bid = Bid(user_id=user_id, lot_id=lot_id, amount=bid_amount)
                session.add(new_bid)
                session.commit()

                QMessageBox.information(self, 'Успешная ставка', 'Ставка успешно размещена.')
                self.load_lots()
                self.update_timer(lot_id)

                print(f'Ставка размещена на лот {lot.name} от пользователя {self.username}: {bid_amount}')
            else:
                QMessageBox.warning(self, 'Ошибка ставки', 'Ставка должна быть выше минимальной цены.')
        else:
            QMessageBox.warning(self, 'Лот закрыт', 'Этот лот больше не принимает ставки.')

    def update_timer(self, lot_id):
        lot = session.query(Lot).filter_by(id=lot_id).first()
        lot.update_timer()
        self.load_lots()
        if lot.is_active():
            QTimer.singleShot(1000, lambda: self.update_timer(lot_id))