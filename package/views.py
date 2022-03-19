'''
    pages.py
    
    - Defines different views for the main window
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class DashboardView(QtWidgets.QWidget):

    '''
        - The main screen to do all Email related activities.
    '''

    logout_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Dashboard - Lynx")
        # Setup UI
        pass


class FingerprintLogin(QtWidgets.QWidget):

    '''
        - Dummy class to attach fingerprint login option
        - This will be implemented in a later stage 
    '''

    def __init__(self):
        super().__init__()
        # Init Widgets
        self.layout = QtWidgets.QVBoxLayout(self)
        self.message = QtWidgets.QLabel()
        self.icon = QtWidgets.QLabel()
        self.fingerprint = QtGui.QPixmap("./package/resources/icons/fingerprint_idle.png")
        self.fingerprint = self.fingerprint.scaledToHeight(128)
        self.icon.setPixmap(self.fingerprint)
        self.message.setFont(QtGui.QFont("Monsterrat", 20, 400))
        self.message.setText("Scan your finger")
        # Configure layout
        self.layout.addWidget(self.icon, 0, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.message, 0, QtCore.Qt.AlignCenter)
        # Set layout
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.setLayout(self.layout)


class ManualLogin(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        # Init UI Elements
        self.sign = QtWidgets.QLabel()
        self.sign.setFont(QtGui.QFont("Monsterrat", 14, 400))
        self.sign.setText("Alternatively, use manual login")
        self.email_input = QtWidgets.QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setPlaceholderText("Password");
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password);
        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.setText("Login")
        # Add UI Elements to Layout
        self.layout.addWidget(self.sign, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        # Set Layout
        self.layout.setContentsMargins(50, 30, 50, 0)
        self.setLayout(self.layout)


class LoginView(QtWidgets.QWidget):

    '''
        - First Screen of the program
        - Contains two options to login
            - Either enter email and password (via keyboard)
            - Or, use fingerprint sensor (only pre-registered users can use this)
        - Also maintains access to database and passes on secrets to Controller once Auth is successful.
    '''

    login_signal = QtCore.pyqtSignal(tuple) # (uname, secret)
    switch_to_registration_signal = QtCore.pyqtSignal()

    def manual_login_action(self):
        self.login_signal.emit(("foobar007@gmail.com", "********"))

    def register(self):
        self.switch_to_registration_signal.emit()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Lynx")
        # Setup login related UI
        self.layout = QtWidgets.QVBoxLayout(self)
        # Init Widgets
        self.header = QtWidgets.QLabel()
        self.header.setText("Login")
        self.header.setFont(QtGui.QFont("Monsterrat", 30, 400))
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        # Setup UI Elements
        self.manual_login = ManualLogin()
        self.fingerprint_login = FingerprintLogin()
        self.manual_login.login_button.clicked.connect(self.manual_login_action)
        self.register_message = QtWidgets.QLabel()
        self.register_message.setText("New User? Register Now!")
        self.register_message.setFont(QtGui.QFont("Monsterrat", 14, 400))
        self.register_button = QtWidgets.QPushButton(self)
        self.register_button.clicked.connect(self.register)
        self.register_button.setText("Register")
        self.register_button.setStyleSheet("color: white; background-color: #1062a8;")
        # Add Widgets to layouts
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.fingerprint_login)
        self.layout.addWidget(self.manual_login)
        self.layout.addWidget(self.register_message, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.register_button, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        # Set layouts
        self.setLayout(self.layout)


class RegistrationView(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration - Lynx")
        # Setup UI
        pass 
