'''
    pages.py
    
    - Defines different views for the main window
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class Dashboard(QtWidgets.QMainWindow):

    '''
        - The main screen to do all Email related activities.
    '''

    logoutSignal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Email Dashboard - Lynx")
        # Set up UI
        pass


class Login(QtWidgets.QMainWindow):

    '''
        - First Screen of the program
        - Contains two options to login
            - Either enter email and password (via keyboard)
            - Or, using fingerprint sensor (only pre-registered users can use this)
        - Also maintains access to database and passes on secrets to Controller once Auth is successful.
    '''

    loginSignal = QtCore.pyqtSignal(tuple) # (uname, secret)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Lynx")
        # Setup login related UI
        pass
