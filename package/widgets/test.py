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
    state = {"idle": True}
    d = FingerprintSensor(state)

    ## Test 2: Enroll a new user
    d.enroll_fingerprint()

    ## Test 3: Test if we can recognize the newly enrolled user
    d.scan()

    # Clear database after tests
    q = input("Do you want to clear the database?\n(y/n):")
    if q.lower() == 'y':
        d.clear_database()

    print("[+] Completed all tests, no error encountered")
