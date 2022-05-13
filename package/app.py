''' 
    app.py 

    - Defines the main controller/window class for the application
    - Controller switches between 'views'
'''

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from package.views import DashboardView, LoginView, RegistrationView
from package.widgets import EmailWidget, FingerprintWidget, DatabaseWidget


# Controller
class MainWindow(QMainWindow):

    '''
        - Runs as the main controller thread
        - Has access to all views and all necessary submodules and coordinates the connection between them.
    '''

    def __init__(self):
        '''
            Initializes the main window with a stacked widget, so we can easily switch between
            different pages (Dashboard, Login, etc).
        '''
        super().__init__()
        self.logger = logging.getLogger(__name__) # Use global default logger
        ''' Setup UI '''
        self.setFixedHeight(600)
        self.setFixedWidth(800)
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
        # Setup Backend Services
        ## Email
        self.email_thread = QtCore.QThread()
        self.email_worker = EmailWidget()
        self.email_worker.moveToThread(self.email_thread)
        ### Setup communication signals with email worker
        self.email_worker.auth_reply_signal.connect(self.login_handler)
        self.email_worker.unread_email_signal.connect(self.add_unread_email)
        self.email_thread.start()
        ## Fingerprint sensor
        self.fps_thread = QtCore.QThread()
        self.fps_state = { "idle": True }
        self.fps_worker = FingerprintWidget(self.fps_state)
        self.fps_worker.moveToThread(self.fps_thread)
        ### Setup communication signals with fingerprint sensor
        self.fps_worker.scan_complete_signal.connect(self.scan_handler)
        self.fps_worker.error_encountered_signal.connect(self.reconnect_fps)
        self.fps_worker.enrollment_stage_one_complete_signal.connect(self.register.continue_enrollment)
        self.fps_worker.enrollment_stage_two_complete_signal.connect(self.enrollment_handler)
        self.fps_thread.start()
        ## Database
        self.db_thread = QtCore.QThread()
        self.db_worker = DatabaseWidget()
        self.db_worker.moveToThread(self.db_thread)
        ### Setup communication singals with database worker
        self.db_worker.added_credentials_signal.connect(self.register.enrollment_complete)
        self.db_worker.fetched_credentials_signal.connect(self.registered_user_login_handler)
        self.db_thread.start()
        # Default to login screen
        self.switch_to_login()

    def add_unread_email(self, email):
        ''' Passes emails to dashboard for display '''
        self.dashboard.add_email(email)

    def enrollment_handler(self, message):
        ''' Adds the credentials to database if the hash is generated '''
        is_finger_enrolled, characteristics_hash = message
        if is_finger_enrolled:
            # Get credentials
            creds = self.register.credential_cache
            details = (creds, characteristics_hash)
            # Add user to databased
            self.logger.debug("Adding new user to database!")
            QtCore.QMetaObject.invokeMethod(self.db_worker, "add_credentials", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(tuple, details))
        else:
            # Update the message on registration screen and try to enroll the finger again
            self.fps_state["idle"] = True
            self.logger.debug("Failed to generate hash!")
            QtCore.QMetaObject.invokeMethod(self.fps_worker, 'enroll_fingerprint', QtCore.Qt.QueuedConnection)
            self.register.repeat_enrollment()

    def reconnect_fps(self):
        ''' Reset the Fingerprint sensor '''
        QtCore.QMetaObject.invokeMethod(self.fps_worker, 'reset_connection', QtCore.Qt.QueuedConnection)

    def scan_handler(self, message):
        ''' Handler fingerprint scan event '''
        is_successful, key = message
        self.fps_state["idle"] = True
        if is_successful:
            # Search for matching hash in database and start
            self.logger.debug("Found a match for the fingerprint!")
            self.logger.debug("Searching for credentials in the database.")
            QtCore.QMetaObject.invokeMethod(self.db_worker, 'fetch_credentials', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, key))
        else:
            # Scan again
            QtCore.QMetaObject.invokeMethod(self.fps_worker, 'scan', QtCore.Qt.QueuedConnection)

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

    def check_login(self, creds):
        ''' Passes credentials to EmailWidget to check if these are valid '''
        self.logger.debug("Checking credentials")
        QtCore.QMetaObject.invokeMethod(self.email_worker, 'check_credentials', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(tuple, creds))

    def registered_user_login_handler(self, message):
        ''' If user credentials were found, pass them to email_worker for login. Else, scan again '''
        found, creds = message
        if found: self.check_login(creds)
        else: QtCore.QMetaObject.invokeMethod(self.fps_worker, 'scan', QtCore.Qt.QueuedConnection)

    def logout_handler(self):
        ''' Clear all credentials '''
        QtCore.QMetaObject.invokeMethod(self.email_worker, 'reset', QtCore.Qt.QueuedConnection)
        self.login.reset()
        self.switch_to_login()

    '''  View Handlers  '''

    def switch_to_login(self):
        ''' Switch to login screen and start Fingerprint Scanning '''
        self.fps_state["idle"] = True
        QtCore.QMetaObject.invokeMethod(self.fps_worker, 'scan', QtCore.Qt.QueuedConnection)
        self.login.reset()
        self.goto("login")

    def switch_to_registration(self):
        self.fps_state["idle"] = True # Stop fingerprint sensor
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
