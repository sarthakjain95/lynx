'''
    mail.py

    - Provides easy API to access an email account
'''

import logging

import email
import imaplib


SMTP_SERVER = "smtp.gmail.com"
SMTP_SERVER_PORT = 465

IMAP_SERVER = "imap.gmail.com"
IMAP_SERVER_PORT = 993


class EmailSession():

    ''' Provides easy access to email services '''

    def __init__(self):
        ''' Starts an IMAP session on given IMAP_SERVER '''
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
            self.imap_session = None
            self.has_valid_creds = False
            return False

    def fetch_unread(self):
        ''' Fetches unread emails from the email server '''
        if self.has_valid_creds:
            try:
                self.session = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_SERVER_PORT)
                _, capabilities = self.session.login(self.email, self.pwd)
                self.logger.info(capabilities)
                self.session.select('inbox')
                retcode, messages = self.session.search(None, 'SEEN')
                if retcode == 'OK':
                    for num in messages[0].split():
                        response_code, data = self.session.fetch(num, '(RFC822)')
                        if response_code == 'OK':
                            # 'data' has a list of tuples (standard_used, content)
                            for response_part in data:
                                if isinstance(response_part, tuple):
                                    mail = email.message_from_bytes(response_part[1])
                                    sub = mail["Subject"]
                                    self.logger.debug(f"Fetched '{sub}' email.")
                                    yield dict(mail.items())
                # Close session and return results
                self.session.close()
            except Exception as err:
                self.imap_session = None # Invalidate current session in case it is still running
                self.logger.error(f"Unknown error occurred [{err}]")
                return
        else:
            # Code should never reach this point under normal circumstances
            return

    def reset(self):
        self.email = None
        self.pwd = None
        self.has_valid_creds = False
