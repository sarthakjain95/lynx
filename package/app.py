''' 
    app.py 

    - Defines the main controller/window class for the application
    - Controller switches between 'views'
'''

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from package.views import DashboardView, LoginView, RegistrationView
from package.widgets import EmailWidget, FingerprintWidget


# Controller
class MainWindow(QMainWindow):

    '''
        - Has access to all views and all necessary submodules and coordinates the connection between them.
    '''

    def __init__(self):
        '''
            Initializes the main window with a stacked widget, so we can easily switch between
            different pages (Dashboard, Login, etc).
        '''
        super().__init__()
        self.logger = logging.getLogger(__name__) # Use global default logger
        self.setFixedHeight(600)
        self.setFixedWidth(800)
        # Setup backend services
        ## Email
        self.email_thread = QtCore.QThread()
        self.email_worker = EmailWidget()
        self.email_worker.moveToThread(self.email_thread)
        ### Set up communication signals with email worker
        self.email_worker.auth_reply_signal.connect(self.login_handler)
        self.email_worker.unread_email_signal.connect(self.add_unread_email)
        self.email_thread.start()
        ## Fingerprint sensor
        self.fps_thread = QtCore.QThread()
        self.fps_state = { "idle": True }
        self.fps_worker = FingerprintWidget(self.fps_state)
        self.fps_worker.moveToThread(self.fps_thread)
        ### Set up communication signals with fingerprint sensor
        self.fps_worker.scan_complete_signal.connect(self.scan_handler)
        self.fps_thread.start()
        # Setup stacked widget
        self.views = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.views)
        # Add views to stack
        self.login = LoginView()
        self.register = RegistrationView()
        self.dashboard = DashboardView()
        self.views.addWidget(self.login)
        self.views.addWidget(self.register)
        self.views.addWidget(self.dashboard)
        # Handle signals
        ## Login
        self.login.login_signal.connect(self.check_login)
        self.login.switch_to_registration_signal.connect(self.switch_to_registration)
        ## Registration
        self.register.check_credentials_signal.connect(self.check_login)
        self.register.switch_to_login_signal.connect(self.switch_to_login)
        ## Dashboard
        self.dashboard.logout_signal.connect(self.logout_handler)
        # Default to login screen
        self.switch_to_login()

    def scan_handler(self, message):
        ''' Handler fingerprint scan event '''
        is_successful, key = message
        if is_successful:
            # Search for matching hash in database and start
            self.logger.debug("Found a match for the fingerprint!")
            self.logger.debug("Searching for credentials in the database.")
        else:
            # Scan again
            self.fps_state["idle"] = True
            QtCore.QMetaObject.invokeMethod(self.fps_worker, 'scan', QtCore.Qt.QueuedConnection)

    def logout_handler(self):
        # Clear all credentials
        QtCore.QMetaObject.invokeMethod(self.email_worker, 'reset', QtCore.Qt.QueuedConnection)
        self.login.reset()
        self.switch_to_login()

    def login_handler(self, has_valid_creds):
        ''' If login credentials are correct, switches view to dashboard '''
        if has_valid_creds:
            self.logger.debug("Given credentials were valid!")
            if self.windowTitle() == self.login.windowTitle():
                self.dashboard.reset()
                self.goto("dashboard")
                # Start fetching emails
                QtCore.QMetaObject.invokeMethod(self.email_worker, 'fetch_unread', QtCore.Qt.QueuedConnection)
            else: # else, this signal is for registration window
                # Promote registration window for fingerprint registration
                self.logger.debug("Starting fingerprint enrollment procedure")
                self.register.enroll_user_fingerprint()
                # Reset email worker
                QtCore.QMetaObject.invokeMethod(self.email_worker, 'reset', QtCore.Qt.QueuedConnection)
                # Start enrollment on fingerprint sensor
                self.fps_state["idle"] = True
                QtCore.QMetaObject.invokeMethod(self.fps_worker, 'enroll_fingerprint', QtCore.Qt.QueuedConnection)
        else:
            self.logger.debug("Invalid credentials encountered!")
            if self.windowTitle() == self.login.windowTitle():
                # Update message on login view
                self.login.invalid_creds()
            else:
                self.register.invalid_creds()

    def add_unread_email(self, email):
        ''' Passes emails to dashboard for display '''
        self.dashboard.add_email(email)

    def check_login(self, creds):
        ''' Passes credentials to EmailWidget to check if these are valid '''
        self.logger.debug("Checking credentials")
        QtCore.QMetaObject.invokeMethod(self.email_worker, 'check_credentials', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(tuple, creds))

    def switch_to_login(self):
        # Start scanning on fingerprint sensor
        self.fps_state["idle"] = True
        QtCore.QMetaObject.invokeMethod(self.fps_worker, 'scan', QtCore.Qt.QueuedConnection)
        self.login.reset()
        self.goto("login")

    def switch_to_registration(self):
        self.register.reset()
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
