''' gmail.py '''

import logging
import imaplib

SERVER = "imap.gmail.com"
PORT = 993

class GmailSession():

    '''
        ** Under Development **
        Provides easy access to gmail services
    '''

    def __init__(self):
        '''Starts an IMAP session on gmail server'''
        self.session = imaplib.IMAP4_SSL(SERVER, PORT)
        self.logger = logging.getLogger(__name__)

    def login(self, email, pwd):
        '''Tries to login the user'''
        try:
            self.session.login(email, pwd)
            self.logger.debug("Successfully logged in!")
            return True
        except Exception as err:
            self.logger.debug("Login attempt was unsuccessful. [%s]", err)
            return False

    def fetch_unread(self):
        '''Fetches all the unread email from gmail'''
        return

    def close(self):
        '''Closes the current session'''
        self.session.close()
        self.session.logout()
