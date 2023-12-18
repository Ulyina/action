import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox

from db.connect import AuctionDatabase
from window.auctioneer_window import AuctioneerWindow
from window.login_window import LoginWindow
from window.registr_window import RegisterWindow
from window.user_interface import UserInterface


class AuctionApp(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация базы данных и создание таблиц
        self.db = AuctionDatabase('auction.db')
        self.db.create_table()
        self.db.create_auction_table()

        self.setWindowTitle("Аукцион")
        self.login_register_layout = QVBoxLayout()

        label = QLabel("Пожалуйста, выберите действие:")
        self.login_register_layout.addWidget(label)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.show_login_window)
        self.login_register_layout.addWidget(self.login_button)

        register_button = QPushButton("Зарегистрироваться")
        register_button.clicked.connect(self.show_register_window)
        self.login_register_layout.addWidget(register_button)

        exit_button = QPushButton("Выйти")
        exit_button.clicked.connect(self.close)
        self.login_register_layout.addWidget(exit_button)

        self.setLayout(self.login_register_layout)

        self.logged_in_user_login = None  # Добавлено для хранения логина пользователя

    def show_login_window(self):
        login_window = LoginWindow(self, "Пользователь", self.db)
        login_window.show()

    def show_register_window(self):
        register_window = RegisterWindow(self, "Пользователь", self.db)
        register_window.show()

    def login(self, window, user_type, login, password):
        if user_type == "Пользователь":
            if self.db.check_user_login(login, password):
                self.show_user_interface(login)
                window.close()
                self.logged_in_user_login = login
            else:
                QMessageBox.warning(window, "Ошибка", "Неверный логин или пароль")
        elif user_type == "Аукционер":
            if self.db.check_auctioneer_login(login, password):
                self.show_auctioneer_interface()
                window.close()
                self.logged_in_user_login = login
            else:
                QMessageBox.warning(window, "Ошибка", "Неверный логин или пароль")

    def register(self, window, user_type, login, password):
        # Регистрация нового пользователя или аукционера в базе данных
        if user_type == "Пользователь":
            self.db.add_user(login, password, user_type)
            QMessageBox.information(window, "Успех", "Пользователь успешно зарегистрирован")
            window.close()
            self.logged_in_user_login = login
        elif user_type == "Аукционер":
            self.db.add_user(login, password, user_type)
            QMessageBox.information(window, "Успех", "Аукционер успешно зарегистрирован")
            window.close()
            self.logged_in_user_login = login

    def show_user_interface(self, login):
        user_interface = UserInterface(self, self.db)
        user_interface.show()

    def show_auctioneer_interface(self):
        auctioneer_window = AuctioneerWindow(self, self.db)
        auctioneer_window.show()
        auctioneer_window.show_item_dialog()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    auction_app = AuctionApp()
    auction_app.show()
    app.auction_app = auction_app  # Сохраняем ссылку на экземпляр в объекте QApplication
    sys.exit(app.exec())
