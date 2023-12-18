from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, \
    QMainWindow, QListWidget, QDialog, QInputDialog, QDialogButtonBox


class AuctioneerWindow(QMainWindow):
    def __init__(self, parent, database):
        super().__init__(parent)
        self.setWindowTitle('Интерфейс аукционера')
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.parent = parent
        self.db = database

        main_layout = QVBoxLayout()

        # Создаем QDialog для отображения товаров
        self.item_dialog = QDialog(self)
        self.item_dialog.setWindowTitle('Товары аукционера')
        self.item_dialog.setGeometry(200, 200, 400, 300)

        item_dialog_layout = QVBoxLayout()
        self.item_list_dialog = QListWidget()
        item_dialog_layout.addWidget(self.item_list_dialog)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.item_dialog.accept)
        item_dialog_layout.addWidget(button_box)
        self.item_dialog.setLayout(item_dialog_layout)

        self.item_list_button = QPushButton('Показать товары')
        self.item_list_button.clicked.connect(self.show_item_dialog)
        main_layout.addWidget(self.item_list_button)

        self.item_list = QListWidget()
        main_layout.addWidget(self.item_list)

        item_info_layout = QVBoxLayout()

        self.item_name_label = QLabel('Наименование товара:')
        item_info_layout.addWidget(self.item_name_label)

        self.item_name_input = QLineEdit()
        item_info_layout.addWidget(self.item_name_input)

        self.start_bid_label = QLabel('Начальная цена:')
        item_info_layout.addWidget(self.start_bid_label)

        self.start_bid_input = QLineEdit()
        item_info_layout.addWidget(self.start_bid_input)

        self.add_item_button = QPushButton('Добавить товар')
        self.add_item_button.clicked.connect(self.add_item)
        item_info_layout.addWidget(self.add_item_button)

        main_layout.addLayout(item_info_layout)

        self.central_widget.setLayout(main_layout)

    def show_item_dialog(self):
        # Получаем товары аукционера из базы данных и обновляем список товаров в диалоге
        items = self.db.get_auctioneer_items(self.parent.logged_in_user_login)
        self.item_list_dialog.clear()
        self.item_list_dialog.addItems(items)
        result = self.item_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            selected_item = self.item_list_dialog.currentItem()
            if selected_item:
                item_id = selected_item.data(0)
                self.show_edit_delete_dialog(item_id)

    def show_edit_delete_dialog(self, item_id):
        edit_delete_dialog = QDialog(self)
        edit_delete_dialog.setWindowTitle('Редактирование/Удаление товара')
        edit_delete_dialog.setGeometry(200, 200, 300, 150)

        edit_delete_layout = QVBoxLayout()

        edit_button = QPushButton('Редактировать')
        edit_button.clicked.connect(lambda: self.edit_item(item_id))
        edit_delete_layout.addWidget(edit_button)

        delete_button = QPushButton('Удалить')
        delete_button.clicked.connect(lambda: self.delete_item(item_id))
        edit_delete_layout.addWidget(delete_button)

        edit_delete_dialog.setLayout(edit_delete_layout)
        edit_delete_dialog.exec()

    def edit_item(self, item_id):
        new_name, ok_name = QInputDialog.getText(self, 'Редактировать товар', 'Введите новое наименование:')
        new_start_bid, ok_start_bid = QInputDialog.getDouble(self, 'Редактировать товар',
                                                             'Введите новую начальную цену:')

        if ok_name and ok_start_bid:
            self.db.cursor.execute('UPDATE items SET item_name=?, start_bid=? WHERE id=?',
                                   (new_name, new_start_bid, item_id))
            self.db.connection.commit()
            self.show_item_dialog()

    def delete_item(self, item_id):
        reply = QMessageBox.question(self, 'Удаление товара', 'Вы уверены, что хотите удалить этот товар?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.db.cursor.execute('DELETE FROM items WHERE id=?', (item_id,))
            self.db.connection.commit()
            self.show_item_dialog()

    def add_item(self):
        item_name = self.item_name_input.text()
        start_bid = self.start_bid_input.text()

        if item_name and start_bid:
            auctioneer_id = self.db.get_user_id(self.parent.logged_in_user_login)  # Получение ID аукционера
            self.db.add_item(auctioneer_id, item_name, start_bid)
            self.item_list.addItem(f'{item_name} - Начальная цена: {start_bid}')
            self.item_name_input.clear()
            self.start_bid_input.clear()
            self.show_item_dialog()  # Используем show_item_dialog вместо show_auctioneer_items
        else:
            QMessageBox.critical(self, 'Ошибка', 'Пожалуйста, введите наименование товара и начальную цену')
