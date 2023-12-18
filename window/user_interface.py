from PyQt6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QMessageBox, QListWidget, QFormLayout, QDialog, QSpinBox


class UserInterface(QDialog):
    def __init__(self, parent, database):
        super().__init__(parent)

        self.setWindowTitle('Интерфейс пользователя')
        self.setGeometry(100, 100, 600, 400)

        self.parent = parent
        self.db = database

        main_layout = QVBoxLayout()

        self.item_list_label = QLabel('Доступные лоты:')
        main_layout.addWidget(self.item_list_label)

        self.item_list = QListWidget()
        main_layout.addWidget(self.item_list)

        item_info_layout = QFormLayout()

        self.selected_item_label = QLabel('Выбранный лот:')
        item_info_layout.addRow(self.selected_item_label, QLabel(''))

        self.min_bid_label = QLabel('Минимальная цена:')
        item_info_layout.addRow(self.min_bid_label, QLabel(''))

        self.bid_label = QLabel('Ваша ставка:')
        item_info_layout.addRow(self.bid_label, QSpinBox())

        self.place_bid_button = QPushButton('Сделать ставку')
        self.place_bid_button.clicked.connect(self.place_bid)
        item_info_layout.addRow(self.place_bid_button)

        main_layout.addLayout(item_info_layout)

        self.setLayout(main_layout)

    def place_bid(self):
        selected_item = self.item_list.currentItem()

        if selected_item:
            item_id = selected_item.data(0)  # Get the item ID from data
            item_name, start_bid, current_bid = self.db.get_item_details(item_id)

            min_bid_label = self.min_bid_label.parent().itemAt(1).widget()
            min_bid_label.setText(f'{start_bid} (Текущая ставка: {current_bid})')

            bid_value = self.bid_label.parent().itemAt(1).widget().value()

            if bid_value > current_bid:
                self.db.place_bid(item_id, bid_value)
                QMessageBox.information(self, 'Ставка размещена',
                                        f'Вы разместили ставку {bid_value} на лот "{item_name}"')
            else:
                QMessageBox.warning(self, 'Ошибка', 'Ставка должна быть выше текущей ставки')
        else:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, выберите лот, на который хотите сделать ставку')
