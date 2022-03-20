'''
    dashboard.py

    - Defines the email dashboard 'view' for this application
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class DashboardView(QtWidgets.QWidget):

    '''
        - The main screen to do all Email related activities.
        - Uses gmail submodule to access emails
    '''

    logout_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Dashboard - Lynx")
        self.layout = QtWidgets.QVBoxLayout(self)
        # Init UI Elements
        self.email_list = QtWidgets.QListWidget(self)
        self.compose_button = QtWidgets.QPushButton(self)
        self.logout_button = QtWidgets.QPushButton(self)
        # Setup widgets
        self.compose_button.setText("Compose")
        self.compose_button.setStyleSheet("color: white; background-color: #1062a8;")
        self.logout_button.setText("Logout")
        self.logout_button.setStyleSheet("color: white; background-color: #d90429;")
        self.logout_button.clicked.connect(self.logout)
        # Add widgets to layout
        self.layout.addWidget(self.email_list)
        self.layout.addWidget(self.compose_button, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.logout_button, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        # Set layout        
        self.setLayout(self.layout)

    def display_emails(self, emails):
        pass

    def logout(self):
        self.logout_signal.emit()
