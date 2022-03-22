''' 
    app.py 

    - Defines the main controller class for the application.
    - Controller switches between 'views'    
'''

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from package.views import DashboardView, LoginView, RegistrationView
from package.widgets import GmailWidget


# Controller
class MainWindow(QMainWindow):

    '''
        (MainWindow) Controller

        - Has access to all views and all necessary submodules and coordinates the connection between them
    '''

    def __init__(self):
        '''
            Initializes the main window with a stacked widget, so we can easily switch between
            different pages (Dashboard, Login, etc).
        '''
        super().__init__()
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        # Setup backend services
        self.gmail_thread = QtCore.QThread()
        self.gmail_worker = GmailWidget()
        self.gmail_worker.moveToThread(self.gmail_thread)
        self.gmail_worker.auth_reply_signal.connect(self.login_handler)
        self.gmail_worker.unread_email_signal.connect(self.add_unread_email)
        self.gmail_thread.start()
        # Setup stacked widget
        self.views = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.views)
        # Add views
        self.login = LoginView()
        self.register = RegistrationView()
        self.dashboard = DashboardView()
        self.views.addWidget(self.login)
        self.views.addWidget(self.register)
        self.views.addWidget(self.dashboard)
        # Handle signals
        self.login.login_signal.connect(self.check_login)
        self.login.switch_to_registration_signal.connect(self.switch_to_registration)
        self.dashboard.logout_signal.connect(self.logout_handler)
        # Default to login screen
        self.switch_to_login()

    def logout_handler(self):
        # Clear all credentials
        self.gmail_worker.reset()
        self.login.reset()
        self.switch_to_login()

    def login_handler(self, has_valid_creds):
        ''' If login credentials are correct, switches view to dashboard '''
        if has_valid_creds:
            self.goto("dashboard")
            # Start fetching emails
            QtCore.QMetaObject.invokeMethod(self.gmail_worker, 'fetch_unread', QtCore.Qt.QueuedConnection)
        else:
            # Update message on login view
            self.login.invalid_creds()

    def add_unread_email(self, email):
        ''' Passes emails to dashboard for display '''
        self.dashboard.add_email(email)

    def check_login(self, creds):
        ''' Passes credentials to GmailWidget to check if these are valid '''
        QtCore.QMetaObject.invokeMethod(self.gmail_worker, 'check_credentials', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(tuple, creds))

    def switch_to_login(self):
        self.goto("login")

    def switch_to_registration(self):
        self.goto("register")

    def goto(self, name):
        ''' Switches screens '''
        if name == "login":
            w = self.login
        elif name == "dashboard":
            w = self.dashboard
        elif name == "register":
            w = self.register
        else:
            print(f"'{name}' does not exist.")
            return
        # Set widget and change title
        self.views.setCurrentWidget(w)
        self.setWindowTitle(w.windowTitle())
