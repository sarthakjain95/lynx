''' 
    app.py 

    - Defines the main controller class for the application.
    - Controller switches between 'views'    
'''

import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from package.views import Dashboard, Login

# Controller
class MainWindow(QMainWindow):

    '''
        ** Under Development **
        Currently used as dummy class to test submodules/widgets
    '''

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
        self.dashboard = Dashboard()
        self.login = Login()
        self.views.addWidget(self.dashboard)
        self.views.addWidget(self.login)
        # Default to login screen
        self.goto("login")

    def goto(self, name):
        ''' Switches screens '''
        match name:
            case "login":
                w = self.login
            case "dashboard":
                w = self.dashboard
        # Set widget and change title
        self.views.setCurrentWidget(w)
        self.setWindowTitle(w.windowTitle())
