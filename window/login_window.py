from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QLineEdit

from window.registr_window import RegisterWindow


class LoginWindow(QWidget):
    def __init__(self, parent, user_type, database):
        super().__init__()

        self.parent = parent
        self.user_type = user_type
        self.db = database

        login_layout = QVBoxLayout()

        user_type_combo = QComboBox()
        user_type_combo.addItem("Пользователь")
        user_type_combo.addItem("Аукционер")
        login_layout.addWidget(user_type_combo)

        login_label = QLabel("Логин:")
        login_layout.addWidget(login_label)

        login_line = QLineEdit()
        login_layout.addWidget(login_line)

        password_label = QLabel("Пароль:")
        login_layout.addWidget(password_label)

        password_line = QLineEdit()
        password_line.setEchoMode(QLineEdit.EchoMode.Password)
        login_layout.addWidget(password_line)

        login_button = QPushButton("Войти")
        login_button.clicked.connect(
            lambda: self.parent.login(self, user_type_combo.currentText(), login_line.text(), password_line.text()))
        login_layout.addWidget(login_button)

        register_button = QPushButton("Зарегистрироваться")
        register_button.clicked.connect(self.show_register_window)
        login_layout.addWidget(register_button)

        exit_button = QPushButton("Выйти")
        exit_button.clicked.connect(self.close)
        login_layout.addWidget(exit_button)

        self.setLayout(login_layout)
        self.setWindowTitle("Вход")

    def show_register_window(self):
        register_window = RegisterWindow(self, self.user_type, self.db)
        register_window.show()
