'''
    R307.py
        - Contains controller class for r307 fingerprint sensor

    [NOTE]:
    Only configured for Windows (COM3) and Linux (/dev/ttyUSB with root privileges)
'''

from sys import platform
import logging

# from pyfingerprint import pyfingerprint
from pyfingerprint.pyfingerprint import PyFingerprint
# from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
# from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2


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
        ''' Enroll a new fingerprint '''
        pass

    def scan(self):
        ''' Keep reading fingerprint until a match is found '''
        pass
