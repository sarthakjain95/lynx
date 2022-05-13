''' widgets/test.py - Tests for submodules '''

import logging

from fps import FingerprintSensor

import base64
from database import Database


def test_database():

    db = Database()

    creds = ("a196c619fa@gmail.com", "0a6baa6ef716d698")
    data = ["00x00", *creds]

    key = "78b955967210c2ea32abfeea1b7aef53"
    b64_key = base64.b64encode(key.encode('ascii'))

    ## Test 1: Encryption/Decryption data
    encrypted_data = db.encrypt(data, b64_key)
    decrypted_data = db.decrypt(encrypted_data, b64_key)
    assert data == decrypted_data

    ## Test 2: Adding credentials to database
    db.add_credentials(creds, key)

    ## Test 3: Retriving credentials from the database
    found, credentials = db.get_credentials(key)
    assert found == True
    assert creds == credentials

    ## Clear Database
    db.erase_everything()

    print("[+] Completed all database tests, no error encountered")


def test_fingerprint_sensor():

    ## Test 1: Make sure we can access the sensor
    state = {"idle": True}
    d = FingerprintSensor(state)

    ## Test 2: Enroll a new user
    d.enroll_fingerprint()

    ## Test 3: Test if we can recognize the newly enrolled user
    d.scan()

    # Clear database after tests
    d.clear_database()

    print("[+] Completed all fingerprint sensor tests, no error encountered")


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

    # Tests
    test_fingerprint_sensor()
    test_database()
