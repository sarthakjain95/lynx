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

    ## Test 2: Enroll a new user
    enrolled = d.enroll_fingerprint()
    if enrolled == False:
        print("[-] Failed to enroll new user")
    else:
        print("[+] Successfully enrolled new user")

    ## Test 3: Test if we can recognize the newly enrolled user
    found, characteristics_hash = d.scan()
    if found == False:
        print("[-] Enrolled user was not found!")
    else:
        print(f"[+] Found user (SHA256:{characteristics_hash})")

    # Clear database after tests
    q = input("Do you want to clear the database?\n(y/n):")
    if q.lower() == 'y':
        d.clear_database()

    print("[+] Completed all tests")
