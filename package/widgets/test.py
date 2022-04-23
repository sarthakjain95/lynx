'''
    widgets/test.py
    
    - Run this to test submodules
'''

import logging
from fps import FingerprintSensor


if __name__ == "__main__":

    # Setup logging
    
    logfile = f"widgets-test-session.log"

    logging.basicConfig(
        format='''%(asctime)s [%(levelname)s] %(message)s''',
        datefmt="%H:%M:%S",
        filename=logfile,
        encoding="utf-8",
        level=logging.DEBUG
    )

    # [r307] Basic Tests
    ## Test 1: Make sure we can access the sensor
    d = FingerprintSensor()
