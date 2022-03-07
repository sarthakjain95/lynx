''' app.py '''

import logging
from PyQt5.QtWidgets import QMainWindow, QPushButton

import package.api.gmail as gmail

class MainWindow(QMainWindow):

    '''
        ** Under Development **
        Currently used as dummy class to test submodules
    '''

    def __init__(self):
        ''' Initializes the main window with a button '''
        super().__init__()
        self.setWindowTitle("Lynx")
        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.do_something)
        self.setCentralWidget(self.button)

    def do_something(self):
        ''' Used to test local submodules '''
        logging.debug("Clicked button!")
        gmail_session = gmail.GmailSession()
        gmail_session.login(None, None)
        # gmail_session.close()
        return
