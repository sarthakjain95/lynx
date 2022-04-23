'''
    widgets.py

    - Contains QObject classes wrapped around submodules
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from .mail import EmailSession
from .fps import FingerprintSensor


class EmailWidget(QtCore.QObject):

    auth_reply_signal = QtCore.pyqtSignal(bool)
    unread_email_signal = QtCore.pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.session = EmailSession()

    @QtCore.pyqtSlot(tuple)
    def check_credentials(self, creds):
        email, pwd = creds
        is_valid = self.session.check_credentials(email, pwd)
        self.auth_reply_signal.emit(is_valid)

    @QtCore.pyqtSlot()
    def fetch_unread(self):
        for email in self.session.fetch_unread():
            self.unread_email_signal.emit(email)

    @QtCore.pyqtSlot()
    def reset(self):
        self.session.reset()


class FingerprintWidget(QtCore.QObject):

    def __init__(self):
        super().__init__()
        pass
