'''
    gmail.py

    - Provides easy API to access a gmail account
'''

import logging
import imaplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_SERVER_PORT = 465

IMAP_SERVER = "imap.gmail.com"
IMAP_SERVER_PORT = 993

class GmailSession():

    '''
        ** Under Development **
        Provides easy access to gmail services
    '''

    def __init__(self):
        '''Starts an IMAP session on gmail IMAP_SERVER'''
        self.logger = logging.getLogger(__name__)
        self.email = None
        self.pwd = None
        self.has_valid_creds = False

    def check_credentials(self, email, pwd):
        try:
            self.imap_session = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_SERVER_PORT)
            self.email = email
            self.pwd = pwd
            self.imap_session.login(email, pwd)
            self.logger.debug("Successfully logged in!")
            self.has_valid_creds = True
            self.imap_session.logout()
            return True
        except Exception as err:
            self.logger.debug("Login attempt was unsuccessful. [%s]", err)
            self.has_valid_creds = False
            return False

    def reset(self):
        self.email = None
        self.pwd = None
        self.has_valid_creds = False
