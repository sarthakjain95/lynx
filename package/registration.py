''' registration.py '''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class FingerprintEnrollmentSection(QtWidgets.QWidget):

    ''' Registration section to enroll the user's fingerprint '''

    def __init__(self):
        super().__init__()
        # Init Layout and Widgets
        self.layout = QtWidgets.QVBoxLayout(self)
        self.error_message = QtWidgets.QLabel()
        self.message = QtWidgets.QLabel()
        self.icon = QtWidgets.QLabel()
        # Set Fingerprint Pixmap
        self.fingerprint = QtGui.QPixmap("./package/resources/icons/fingerprint_idle.png")
        self.fingerprint = self.fingerprint.scaledToHeight(128)
        self.icon.setPixmap(self.fingerprint)
        # Configure Text and Font Style
        self.error_message.setFont(QtGui.QFont("Monsterrat", 12, 200))
        self.error_message.setStyleSheet("color:red;")
        self.message.setFont(QtGui.QFont("Monsterrat", 20, 400))
        self.reset() # Reset text
        # Configure layout
        self.layout.addWidget(self.icon, 0, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.error_message, 0, QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.message, 0, QtCore.Qt.AlignCenter)
        # Set layout
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.setLayout(self.layout)

    def rescan_message(self):
        self.error_message.setText("")
        self.message.setText("Please scan you finger one more time!")

    def enrollment_complete(self):
        self.icon.setVisible(False)
        self.message.setText("Registration Complete!")

    def repeat_enrollment(self):
        ''' Display general message and error message '''
        self.reset()
        self.error_message.setText("Could not enroll your finger! Please try again!")

    def reset(self):
        ''' Reset all text on this screen to initial state '''
        self.icon.setVisible(True)
        self.error_message.setText("")
        self.message.setText("Please scan your finger")


class CredentialsInputSection(QtWidgets.QWidget):

    ''' Registration section for collecting and validating user's credentials '''

    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        # Init UI Elements
        self.sign = QtWidgets.QLabel()
        self.sign.setFont(QtGui.QFont("Monsterrat", 14, 400))
        self.sign.setText("Enter your credentials")
        self.email_input = QtWidgets.QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setPlaceholderText("Password");
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password);
        self.check_cred_button = QtWidgets.QPushButton(self)
        self.check_cred_button.setText("Check Credentials")
        # Add UI Elements to Layout
        self.layout.addWidget(self.sign, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.check_cred_button)
        # Set Layout
        self.layout.setContentsMargins(50, 30, 50, 0)
        self.setLayout(self.layout)

    def display_error(self):
        # Display error message
        self.sign.setFont(QtGui.QFont("Monsterrat", 14, 300))
        self.sign.setText("Invalid Credentials, Try Again.")
        self.sign.setStyleSheet("color:red;")

    def reset(self):
        # Clear inputs
        self.email_input.clear()
        self.password_input.clear()
        # Reset sign text and font
        self.sign.setFont(QtGui.QFont("Monsterrat", 14, 400))
        self.sign.setText("Enter your credentials")
        self.sign.setStyleSheet("color:black;")


class RegistrationView(QtWidgets.QWidget):

    '''
        - Registration screen for new users
        - These are the steps for registration:
            - Firstly, enter your credentials for accessing the imap server (These will also be checked).
            - Then, enroll your fingerprint using the fingerprint sensor
            - After this, the hash generated from fingerprint sensor is used to encrypt the login info, which
                is then saved to a local database
    '''

    check_credentials_signal = QtCore.pyqtSignal(tuple)
    switch_to_login_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registration - Lynx")
        # Setup login related UI
        self.layout = QtWidgets.QVBoxLayout(self)
        # Init Widgets
        self.header = QtWidgets.QLabel()
        self.header.setText("Register")
        self.header.setFont(QtGui.QFont("Monsterrat", 30, 400))
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        # Setup UI Elements
        self.view_stack = QtWidgets.QStackedWidget()
        self.credentials_input_section = CredentialsInputSection()
        self.fingerprint_enrollment_section = FingerprintEnrollmentSection()
        self.credentials_input_section.check_cred_button.clicked.connect(self.check_credentials_action)
        self.view_stack.addWidget(self.credentials_input_section)
        self.view_stack.addWidget(self.fingerprint_enrollment_section)
        self.view_stack.setCurrentWidget(self.credentials_input_section)
        # Subsection
        self.login_message = QtWidgets.QLabel()
        self.login_message.setText("Already have an account? Login Instead!")
        self.login_message.setFont(QtGui.QFont("Monsterrat", 14, 400))
        self.login_button = QtWidgets.QPushButton(self)
        self.login_button.clicked.connect(self.login)
        self.login_button.setText("Login")
        self.login_button.setStyleSheet("color: white; background-color: #1062a8;")
        # Add Widgets to layouts
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.view_stack, 0, QtCore.Qt.AlignBottom)
        self.layout.addWidget(self.login_message, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.login_button, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter)
        # Set layouts
        self.setLayout(self.layout)

    def login(self): # Switch to login window
        self.switch_to_login_signal.emit()

    ''' Fingerprint Sensor '''

    def enroll_user_fingerprint(self):
        # Reset all widgets
        self.reset()
        # Switch to fingerprint scanning mode
        self.view_stack.setCurrentWidget(self.fingerprint_enrollment_section)

    def continue_enrollment(self):
        # Update message on fingerprint scanning section
        self.fingerprint_enrollment_section.rescan_message()

    def enrollment_complete(self):
        # User enrollment is complete, display success message
        self.fingerprint_enrollment_section.enrollment_complete()

    def repeat_enrollment(self):
        # Display error message and ask user to re-enroll fingerprint
        self.fingerprint_enrollment_section.repeat_enrollment()

    ''' Login Screen '''

    def invalid_creds(self):
        # Display error message
        self.credentials_input_section.display_error()
        # Enable buttons
        self.credentials_input_section.check_cred_button.setEnabled(True)
        self.login_button.setEnabled(True)

    def check_credentials_action(self):
        email = self.credentials_input_section.email_input.text().strip()
        pwd = self.credentials_input_section.password_input.text().strip()
        if len(email) > 0 and len(pwd) > 0:
            # Disable buttons so user cannot spam 'check_credentials_signal'
            self.credentials_input_section.check_cred_button.setEnabled(False)
            self.login_button.setEnabled(False)
            # Send credentials back to controller for validation
            self.check_credentials_signal.emit((email, pwd))

    ''' Reset '''

    def reset(self):
        # Reset to credentials input section
        self.view_stack.setCurrentWidget(self.credentials_input_section)
        # Reset CredentialsInputSection
        self.credentials_input_section.reset()
        # Enable buttons
        self.credentials_input_section.check_cred_button.setEnabled(True)
        self.login_button.setEnabled(True)
