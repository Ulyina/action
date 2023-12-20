import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox, \
    QListWidget, QListWidgetItem, QInputDialog
from PyQt5.QtCore import Qt, QTimer
from sqlalchemy import create_engine, Column, String, Integer, Enum, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from bd.connect import Lot, session


class AuctioneerWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Привет, аукционер {self.username}')
        self.setGeometry(200, 200, 800, 400)

        layout = QVBoxLayout()

        self.name_label = QLabel('Название лота:')
        self.name_input = QLineEdit(self)

        self.description_label = QLabel('Описание лота:')
        self.description_input = QLineEdit(self)

        self.min_price_label = QLabel('Минимальная цена:')
        self.min_price_input = QLineEdit(self)

        self.timer_label = QLabel('Таймер (сек):')
        self.timer_input = QLineEdit(self)

        self.create_lot_button = QPushButton('Создать лот', self)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_input)
        layout.addWidget(self.min_price_label)
        layout.addWidget(self.min_price_input)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.timer_input)
        layout.addWidget(self.create_lot_button)

        self.create_lot_button.clicked.connect(self.create_lot)

        self.setLayout(layout)

    def create_lot(self):
        name = self.name_input.text()
        description = self.description_input.text()
        min_price = float(self.min_price_input.text())
        timer_seconds = int(self.timer_input.text())

        new_lot = Lot(name=name, description=description, min_price=min_price, timer_seconds=timer_seconds)
        new_lot.timer = QTimer()
        new_lot.timer.timeout.connect(new_lot.update_timer)
        new_lot.timer.start(1000)
        session.add(new_lot)
        session.commit()

        QMessageBox.information(self, 'Успешное создание лота', 'Лот успешно создан.')

        print(f'Лот создан: {name}, {description}, Минимальная цена: {min_price}, Таймер: {timer_seconds} сек')