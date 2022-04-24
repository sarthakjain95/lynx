'''
    R307.py
    
    - Contains controller class for r307 fingerprint sensor

    [NOTE]:
    Only configured for Windows (COM3) and Linux (/dev/ttyUSB with root privileges)
'''

from sys import platform
import logging
import time
import hashlib

# from pyfingerprint import pyfingerprint
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2


class R307():

    BAUD_RATE = 115200 # Do not change

    def __init__(self):
        self.logger = logging.getLogger(__name__) # Use global default logger
        self.set_port() # Set port
        # Open a connection to r307
        self.logger.info(f"Opening a serial connection to '{self.port}'")
        self.dev = PyFingerprint(self.port, self.BAUD_RATE)
        # Make sure connection was successful
        if self.dev.verifyPassword() == False:
            self.logger.error("Could not connect to the fingerprint sensor")
            raise Exception("Could not connect")
        self.logger.info("Successfully connected to the fingerprint sensor")

    def set_port(self):
        ''' Set access port based on OS '''
        if 'linux' in platform.lower():
            self.port = "/dev/ttyUSB0"
        elif 'win' in platform.lower():
            self.port = "COM3"
        else:
            raise Exception("Could not set port")
        # Log final selection
        self.logger.info(f"Setting port to {self.port}")

    def enroll_fingerprint(self):
        '''
            - Enroll a new fingerprint
            - Keeps running until a finger enrolled (2 successful scans)
            - Returns True if both fingers matched, otherwise returns False
        '''

        # Scan 1
        self.logger.debug("Enrolling new user")
        while(self.dev.readImage() == False):
            continue

        # Save new scan characteristics to buffer
        self.dev.convertImage(FINGERPRINT_CHARBUFFER1)
        self.logger.debug("First scan complete")

        time.sleep(2)

        # Scan 2
        while(self.dev.readImage() == False):
            continue

        # Save new scan characteristics to buffer
        self.dev.convertImage(FINGERPRINT_CHARBUFFER2)
        self.logger.debug("Second scan complete")

        if self.dev.compareCharacteristics() == 0:
            # Fingers do not match, we cannot add this template to database
            return False

        # Add this template to database
        self.dev.createTemplate()
        position = self.dev.storeTemplate()

        return True

    def scan(self):
        '''
            - Read a fingerprint and tries to match it with an existing template in the database
            - If a match is found, returns the hash of the characteristics of matching template
        '''

        while(self.dev.readImage() == False):
            continue

        self.dev.convertImage(FINGERPRINT_CHARBUFFER1)
        position, accuracy = self.dev.searchTemplate()

        if position == -1 or accuracy < 0.5:
            return False, None

        # Load characteristics in buffer and compute hash
        self.dev.loadTemplate(position, FINGERPRINT_CHARBUFFER1)
        characteristics = self.dev.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)
        characteristics = str(characteristics).encode('utf-8')
        characteristics_hash = hashlib.sha256(characteristics).hexdigest()

        return True, characteristics_hash

    # Test only
    def clear_database(self):
        ''' Clears all saved fingerprint '''
        self.logger.info("Clearing fingerprint database.")
        self.dev.clearDatabase()
