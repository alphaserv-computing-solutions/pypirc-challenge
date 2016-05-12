"""Challenge encrypter and decrypter functions

Notes on security: ECB is not entirely secure, however, unless there is a
server that can encrypt and pass nonces on the other side, this is probably
the only option
"""

import base64

from Crypto.Cipher import AES


def pad256(key):
    """Pad a key to 256 bits"""
    padlen = 32 - len(key)
    if padlen < 0:
        raise ValueError('key should be 32 characters')
    key += padlen * chr(0)
    return key


def encrypt(password, key):
    """Encrypts password with a key and returns the base64 encoded string"""
    ciph = AES.new(pad256(key), AES.MODE_ECB)
    return base64.b64encode(ciph.encrypt(password))


def decrypt(passblob64, key):
    """Decrypts a base64 encoded string with a key"""
    ciph = AES.new(pad256(key), AES.MODE_ECB)
    return ciph.decrypt(base64.b64decode(passblob64))
