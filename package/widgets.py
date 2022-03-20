'''
    widgets.py

    - Contains QObject classes wrapped around submodules
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from package.api.gmail import GmailSession


class GmailWidget(QtCore.QObject):

    auth_reply_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.session = GmailSession()

    def check_credentials(self, email, pwd):
        is_valid = self.session.check_credentials(email, pwd)
        self.auth_reply_signal.emit(is_valid)

    def reset(self):
        self.session.reset()
