import os
import hashlib


def hashing(password: str) -> tuple:
    salt = os.urandom(32)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000, )
    hex_hash = digest.hex()
    del(password)
    return (salt, hex_hash)


def checking(salt: str, hash: str, password: str) -> bool:
    test = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 1000, )
    hex_hash_test = test.hex()
    del(password)
    if hex_hash_test == hash:
        return True
    else:
        return False
