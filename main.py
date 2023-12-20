import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QMessageBox

from bd.connect import session, User
from window.auctioneer_window import AuctioneerWindow
from window.user_window import UserWindow


class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Авторизация')
        self.setGeometry(200, 200, 800, 400)

        layout = QVBoxLayout()

        self.username_label = QLabel('Имя пользователя:')
        self.username_input = QLineEdit(self)

        self.password_label = QLabel('Пароль:')
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.role_label = QLabel('Роль:')
        self.role_combobox = QComboBox()
        self.role_combobox.addItems(['User', 'Auctioneer'])

        self.login_button = QPushButton('Войти', self)
        self.register_button = QPushButton('Зарегистрироваться', self)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.role_label)
        layout.addWidget(self.role_combobox)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combobox.currentText().lower()

        user = session.query(User).filter_by(username=username, password=password, role=role).first()

        if user:
            if role == 'auctioneer':
                self.open_auctioneer_window(username)
            else:
                self.open_user_window(username)
        else:
            print('Неверные данные для входа')

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_combobox.currentText().lower()

        new_user = User(username=username, password=password, role=role)
        session.add(new_user)
        session.commit()

        QMessageBox.information(self, 'Успешная регистрация', f'Пользователь {username} успешно зарегистрирован.')

        print(f'Пользователь зарегистрирован: {username}')

    def open_user_window(self, username):
        self.user_window = UserWindow(username)
        self.user_window.show()

    def open_auctioneer_window(self, username):
        self.auctioneer_window = AuctioneerWindow(username)
        self.auctioneer_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec_())
