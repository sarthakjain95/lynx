''' 
    app.py 

    - Defines the main controller class for the application.
    - Controller switches between 'views'    
'''

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from package.views import DashboardView, LoginView, RegistrationView

# Controller
class MainWindow(QMainWindow):

    '''
        ** Under Development **
        Currently used as dummy class to test submodules/widgets
    '''

    def login_handler(self, info):
        print(info)
        self.goto("dashboard")

    def __init__(self):
        '''
            Initializes the main window with a stacked widget, so we can easily switch between
            different pages (Dashboard, Login, etc).
        '''
        super().__init__()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        # Setup stacked widget
        self.views = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.views)
        # Add views
        self.dashboard = DashboardView()
        self.login = LoginView()
        self.register = RegistrationView()
        self.views.addWidget(self.dashboard)
        self.views.addWidget(self.login)
        self.views.addWidget(self.register)
        # Handle signals
        self.login.login_signal.connect(self.login_handler)
        self.login.switch_to_registration_signal.connect(self.switchToRegister)
        # Default to login screen
        self.goto("login")

    def switchToRegister(self):
        self.goto("register")

    def goto(self, name):
        ''' Switches screens '''
        match name:
            case "login":
                w = self.login
            case "dashboard":
                w = self.dashboard
            case "register":
                w = self.register
            case _:
                print(f"'{name}' does not exist.")
                return
        # Set widget and change title
        self.views.setCurrentWidget(w)
        self.setWindowTitle(w.windowTitle())
