'''
    R307.py
    
    - Contains controller class for r307 fingerprint sensor
    - R307 inherits from QtCore.QObject because we have to embed signals at every stage of
        fingerprint scanning/enrollment. Handling errors and passing status messages would
        be more complicated if we depend on a wrapper class for message passing.

    [NOTE]:
    Only configured for Windows (COM3) and Linux (/dev/ttyUSB with root privileges)
'''

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

from sys import platform
import logging
import time
import hashlib

# from pyfingerprint import pyfingerprint
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2


class R307(QtCore.QObject):

    '''
        R307 - Handles basic operations on r307
        Args:
            state:dictionary
                - Passed and maintained by Controller
                - Since python dictionaries are thread safe and mutable, they can be used to
                    easily get out of a while loop running in another QThread.
                - Should contain the key 'idle' mapped to a boolean value
    '''

    # Signals
    scan_complete_signal = QtCore.pyqtSignal(tuple)
    enrollment_stage_one_complete_signal = QtCore.pyqtSignal()
    enrollment_state_two_complete_signal = QtCore.pyqtSignal(tuple)
    error_encountered_signal = QtCore.pyqtSignal(str)

    BAUD_RATE = 115200 # Do not change

    def __init__(self, state):
        super().__init__()
        self.state = state
        self.logger = logging.getLogger(__name__) # Use global default logger
        self.reset_connection() # Sets connection

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

    @QtCore.pyqtSlot()
    def reset_connection(self):
        ''' Resets the connection to fingerprint sensor '''
        try:
            # Make sure previous connection session is discarded
            self.dev = None
            time.sleep(1)
            # Reset port
            self.set_port()
            # Open a connection to r307
            self.logger.info(f"Opening a serial connection to '{self.port}'")
            self.dev = PyFingerprint(self.port, self.BAUD_RATE)
            # Make sure connection was successful
            if self.dev.verifyPassword() == False:
                raise Exception("Could not connect to the fingerprint sensor!")
            self.logger.info("Successfully connected to the fingerprint sensor!")
        except Exception as e:
            e_message = str(e)
            self.logger.error(f"Error Encountered: {e_message}")
            self.error_encountered.emit(e_message)

    @QtCore.pyqtSlot()
    def enroll_fingerprint(self):
        '''
            - Enroll a new fingerprint
            - Keeps running until a finger enrolled (2 successful scans)
            - Returns True if both fingers matched, otherwise returns False
        '''
        self.state["idle"] = False
        try:
            # Scan 1
            self.logger.debug("Enrolling new user")
            while(self.dev.readImage() == False):
                if self.state["idle"]: # Check if controller wants to stop this loop
                    self.logger.debug(f"State:Idle encountered! Scanning Stopped.")
                    return
                continue

            # Save new scan characteristics to buffer
            self.dev.convertImage(FINGERPRINT_CHARBUFFER1)
            self.logger.debug("First scan complete")
            self.enrollment_stage_one_complete_signal.emit()

            time.sleep(2)

            # Scan 2
            while(self.dev.readImage() == False):
                if self.state["idle"]:
                    self.logger.debug(f"State:Idle encountered! Scanning Stopped.")
                    return
                continue

            # Save new scan characteristics to buffer
            self.dev.convertImage(FINGERPRINT_CHARBUFFER2)
            self.logger.debug("Second scan complete")

            if self.dev.compareCharacteristics() == 0:
                # Fingers do not match, we cannot add this template to database
                self.enrollment_state_two_complete_signal.emit((False, None))
                self.logger.info("Fingers do not match! Cannot enroll user.")
                return

            # Add this template to database
            self.dev.createTemplate()
            position = self.dev.storeTemplate()

            # Convert characteristics to hash
            characteristics = self.dev.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)
            characteristics = str(characteristics).encode('utf-8')
            characteristics_hash = hashlib.sha256(characteristics).hexdigest()

            # Send the hash back to controller
            self.logger.debug(f"Caputured hash {characteristics_hash[:8]}*")
            self.enrollment_state_two_complete_signal.emit((True, characteristics_hash))
            return
        except Exception as e:
            e_message = str(e)
            self.logger.debug("Encountered error while enrolling finger: " + e_message)
            self.error_encountered_signal.emit(e_message)

    @QtCore.pyqtSlot()
    def scan(self):
        '''
            - Reads a fingerprint and tries to match it with an existing template in the database
            - If a match is found, returns the hash of the characteristics of matching template
        '''
        self.state['idle'] = False # Reset this to false, since scan is just called!
        try:
            self.logger.debug("Scanning finger!")
            while self.dev.readImage() == False:
                if self.state["idle"]: # Check if controller wants to stop this loop
                    self.logger.debug(f"State:Idle encountered! Scanning Stopped.")
                    return
                continue

            self.dev.convertImage(FINGERPRINT_CHARBUFFER1)
            position, accuracy = self.dev.searchTemplate()

            if position == -1 or accuracy < 0.5:
                self.logger.debug("No match found!")
                self.scan_complete_signal.emit((False, None))
                return

            # Load characteristics in buffer and compute hash
            self.dev.loadTemplate(position, FINGERPRINT_CHARBUFFER1)
            characteristics = self.dev.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)
            characteristics = str(characteristics).encode('utf-8')
            characteristics_hash = hashlib.sha256(characteristics).hexdigest()

            self.logger.debug(f"Found match: {characteristics_hash[:8]}*")
            self.scan_complete_signal.emit((True, characteristics_hash))
            return
        except Exception as e:
            e_message = str(e)
            self.logger.debug("Encountered error while scanning finger: " + e_message)
            self.error_encountered_signal.emit(e_message)

    # Used for tests only
    def clear_database(self):
        ''' Clears all saved fingerprint '''
        self.logger.info("Clearing fingerprint database.")
        self.dev.clearDatabase()
