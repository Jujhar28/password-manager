from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class LoginWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.username_label = QLabel("Username:")
        self.password_label = QLabel("Password:")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.main_window.verify_user(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            # Check if the username already exists
            if not self.main_window.user_exists(username):
                # Register the new user
                self.main_window.register_user(username, password)
                QMessageBox.information(self, "Registration Successful", "You are now registered.")
            else:
                QMessageBox.warning(self, "Registration Failed", "Username already exists.")
        else:
            QMessageBox.warning(self, "Registration Failed", "Please enter a username and password.")
