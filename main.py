import sys
import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QMessageBox, QTextEdit, QComboBox, QHBoxLayout, QGroupBox, QRadioButton, QDialog
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from login import LoginWindow  # Import the LoginWindow class from login.py

class PasswordManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.conn = self.connect_to_database()
        self.create_password_table()
        self.load_websites()

    def init_ui(self):
        self.setWindowTitle('Password Manager By Jujhar28')
        self.setGeometry(100, 100, 400, 400)

        # Initialize the theme to light mode
        self.dark_mode = False

        # Create a central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create a theme toggle button
        self.theme_toggle = QRadioButton("Dark Mode")
        self.theme_toggle.clicked.connect(self.toggle_theme)
        self.layout.addWidget(self.theme_toggle)

        # Rest of the UI elements
        self.website_label = QLabel('Website:')
        self.new_website_label = QLabel('New Website:')
        self.username_label = QLabel('Username:')
        self.password_label = QLabel('Password:')

        # Apply custom label styles
        label_font = QFont("Arial", 12)
        label_font.setBold(True)
        self.website_label.setFont(label_font)
        self.new_website_label.setFont(label_font)
        self.username_label.setFont(label_font)
        self.password_label.setFont(label_font)

        self.website_input = QComboBox()
        self.new_website_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.add_button = QPushButton('Add Password')
        self.edit_button = QPushButton('Edit Password')
        self.delete_button = QPushButton('Delete Password')
        self.retrieve_button = QPushButton('Retrieve Passwords')
        self.passwords_display = QVBoxLayout()

        # Apply custom button styles
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.edit_button.setCursor(Qt.PointingHandCursor)
        self.delete_button.setCursor(Qt.PointingHandCursor)
        self.retrieve_button.setCursor(Qt.PointingHandCursor)

        # Add edit and delete buttons to a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addWidget(self.website_label)
        self.layout.addWidget(self.website_input)
        self.layout.addWidget(self.new_website_label)
        self.layout.addWidget(self.new_website_input)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.add_button)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.retrieve_button)

        # Set modern and clean look for the password display
        self.passwords_display.setContentsMargins(10, 10, 10, 10)
        self.passwords_display.setAlignment(Qt.AlignTop)
        self.passwords_display.setSpacing(10)

        self.layout.addLayout(self.passwords_display)

        self.add_button.clicked.connect(self.add_password)
        self.edit_button.clicked.connect(self.edit_password)
        self.delete_button.clicked.connect(self.delete_password)
        self.retrieve_button.clicked.connect(self.retrieve_passwords)
        self.website_input.currentIndexChanged.connect(self.on_website_changed)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            # Dark mode styles
            self.setStyleSheet("""
                background-color: #333333;
                color: #FFFFFF;
            """)
        else:
            # Light mode styles
            self.setStyleSheet("""
                background-color: #FFFFFF;
                color: #000000;
            """)

    def connect_to_database(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="jujh@r2831",
                database="password_manager"
            )
            return conn
        except Exception as e:
            QMessageBox.critical(self, "Database Error", "Error connecting to the database: " + str(e))
            sys.exit(1)

    def create_password_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INT AUTO_INCREMENT PRIMARY KEY,
                website VARCHAR(255) NOT NULL,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        self.conn.commit()

    def load_websites(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT DISTINCT website FROM passwords")
        websites = cursor.fetchall()
        self.website_input.clear()
        self.website_input.addItem("New Website")
        self.website_input.addItems([website[0] for website in websites])

    def add_password(self):
        website = self.website_input.currentText()
        new_website = self.new_website_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if new_website:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO passwords (website, username, password)
                VALUES (%s, %s, %s)
            """, (new_website, username, password))
            self.conn.commit()
            self.load_websites()
            self.new_website_input.clear()

        elif website and username and password:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO passwords (website, username, password)
                VALUES (%s, %s, %s)
            """, (website, username, password))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Password added successfully!")
            self.username_input.clear()
            self.password_input.clear()
            self.load_websites()

        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")

    def edit_password(self):
        website = self.website_input.currentText()
        username = self.username_input.text()
        password = self.password_input.text()

        if website and username and password:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE passwords
                SET username = %s, password = %s
                WHERE website = %s
            """, (username, password, website))
            self.conn.commit()
            QMessageBox.information(self, "Success", "Password edited successfully!")
            self.load_websites()
        else:
            QMessageBox.warning(self, "Input Error", "Please select a website and fill in all fields.")

    def delete_password(self):
        website = self.website_input.currentText()

        if website:
            confirm = QMessageBox.question(self, "Confirm Deletion", f"Are you sure you want to delete all passwords for {website}?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                cursor = self.conn.cursor()
                cursor.execute("""
                    DELETE FROM passwords
                    WHERE website = %s
                """, (website,))
                self.conn.commit()
                QMessageBox.information(self, "Success", f"All passwords for {website} deleted successfully!")
                self.load_websites()
        else:
            QMessageBox.warning(self, "Input Error", "Please select a website.")

    def retrieve_passwords(self):
        website = self.website_input.currentText()
        if website:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT username, password FROM passwords
                WHERE website = %s
            """, (website,))
            passwords = cursor.fetchall()

            if passwords:
                # Clear the previous display
                for i in reversed(range(self.passwords_display.count())):
                    self.passwords_display.itemAt(i).widget().setParent(None)

                # Create a group box for each password entry
                for username, password in passwords:
                    group_box = QGroupBox(f"Website: {website}")
                    layout = QVBoxLayout()
                    layout.addWidget(QLabel(f"Username: {username}"))
                    layout.addWidget(QLabel(f"Password: {password}"))
                    group_box.setLayout(layout)

                    # Add the group box to the display
                    self.passwords_display.addWidget(group_box)
            else:
                self.passwords_display.addWidget(QLabel(f"No passwords found for {website}."))
        else:
            QMessageBox.warning(self, "Input Error", "Please select a website.")

    def on_website_changed(self, index):
        selected_website = self.website_input.currentText()

        # Show the New Website input field when "New Website" is selected
        if selected_website == "New Website":
            self.new_website_label.show()
            self.new_website_input.show()
        else:
            self.new_website_label.hide()
            self.new_website_input.hide()

    def verify_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM users
            WHERE username = %s AND password_hash = %s
        """, (username, password))
        return cursor.fetchone() is not None

    def user_exists(self, username):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM users
            WHERE username = %s
        """, (username,))
        return cursor.fetchone() is not None

    def register_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """, (username, password))
        self.conn.commit()

def main():
    app = QApplication(sys.argv)
    main_window = PasswordManagerApp()
    login_window = LoginWindow(main_window)  # Pass main_window instance
    if login_window.exec_() == QDialog.Accepted:
        main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = PasswordManagerApp()
    login_window = LoginWindow(main_window)  # Pass main_window instance
    if login_window.exec_() == QDialog.Accepted:
        main_window.show()
    sys.exit(app.exec_())
