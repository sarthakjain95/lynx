''' 
    database.py 
    
    - Contains handler class for database used in this project 
    - By default, database is set to 'database.json' in the project root directory
'''

import logging

import base64
from cryptography.fernet import Fernet
from tinydb import TinyDB, Query


class DatabaseSession():

    PUBLIC_KEY = "lynx"
    DATABASE_PATH = "./database.json"

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.db = TinyDB(self.DATABASE_PATH)

    def encrypt(self, data, key):
        '''
            data: given list of strings to be encrypted
            key: base64 encoded key
        '''
        f, results = Fernet(key), []
        for s in data:
            token = f.encrypt(bytes(s, 'utf-8'))
            results.append(token.decode('ascii'))
        return results

    def decrypt(self, data, key):
        f, results = Fernet(key), []
        for s in data:
            try:
                token = f.decrypt(bytes(s, 'utf-8'))
                results.append(token.decode('ascii'))
            except:
                results.append("0x0")
        return results

    def add_credentials(self, creds, encryption_key):
        b64_key = base64.b64encode(encryption_key.encode('ascii'))
        public_key, email, pwd = self.encrypt([self.PUBLIC_KEY, *creds], b64_key)
        # Add encrypted credentials to database
        encrypted_credentials = {
            'key': public_key,
            'email': email,
            'password': pwd
        }
        self.db.insert(encrypted_credentials)
        self.logger.debug("Added new user to the database!")

    def get_credentials(self, decryption_key):
        b64_key = base64.b64encode(decryption_key.encode('ascii'))
        for item in self.db:
            key = item['key']
            decoded_key = self.decrypt([key], b64_key)[0]
            if decoded_key == self.PUBLIC_KEY:
                # Get credentials
                email, pwd = item['email'], item['password']
                email, pwd = self.decrypt([email, pwd], b64_key)
                self.logger.debug("Found user record!")
                return (True, (email, pwd))
        # User not found!
        self.logger.debug("Could not find the user!")
        return (False, None)

    # Only used for tests
    def erase_everything(self):
        self.db.truncate()
