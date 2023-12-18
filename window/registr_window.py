from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QComboBox, QLineEdit


class RegisterWindow(QWidget):
    def __init__(self, parent, user_type, database):
        super().__init__()

        self.parent = parent
        self.user_type = user_type
        self.db = database

        register_layout = QVBoxLayout()

        user_type_combo = QComboBox()
        user_type_combo.addItem("Пользователь")
        user_type_combo.addItem("Аукционер")
        register_layout.addWidget(user_type_combo)

        login_label = QLabel("Логин:")
        register_layout.addWidget(login_label)

        login_line = QLineEdit()
        register_layout.addWidget(login_line)

        password_label = QLabel("Пароль:")
        register_layout.addWidget(password_label)

        password_line = QLineEdit()
        password_line.setEchoMode(QLineEdit.EchoMode.Password)
        register_layout.addWidget(password_line)

        register_button = QPushButton("Зарегистрироваться")
        register_button.clicked.connect(
            lambda: self.parent.register(self, user_type_combo.currentText(), login_line.text(), password_line.text()))
        register_layout.addWidget(register_button)

        exit_button = QPushButton("Выйти")
        exit_button.clicked.connect(self.close)
        register_layout.addWidget(exit_button)

        self.setLayout(register_layout)
        self.setWindowTitle("Регистрация")
