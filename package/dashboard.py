'''
    dashboard.py

    - Defines the email dashboard view for this application
'''

from PyQt5 import QtCore, QtWidgets


class DashboardView(QtWidgets.QWidget):

    ''' The main screen to do all Email related activities '''

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

    def add_email(self, email):
        ''' Adds the given email's 'Subject' to the list '''
        self.email_list.addItem(email["Subject"])

    def logout(self):
        self.email_list.clear()
        self.logout_signal.emit()

    def reset(self):
        ''' Clear the list of emails '''
        self.email_list.clear()
