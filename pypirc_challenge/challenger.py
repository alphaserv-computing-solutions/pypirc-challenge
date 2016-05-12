"""Challenge encrypter and decrypter functions

Notes on security:
ECB (default with no challenge) is not entirely secure, however, unless
there is a server that can encrypt and pass nonces on the other side,
this is probably the only option
If a challenge is provided, the remote endpoint must use CBC to encrypt
the file before transport
"""

import base64
import os

from Crypto.Cipher import AES


def generate_challenge():
    """Generate a 256 bit random nonce"""
    return base64.b64encode(os.urandom(32))[:32]


def _pad256(key):
    """Pad a key to 256 bits"""
    padlen = 32 - len(key)
    if padlen < 0:
        raise ValueError('key should be 32 characters')
    key += padlen * chr(0)
    return key


def _get_ciph(key, challenge=None):
    """Generates an AES cipher using a key

    If a challenge is provided, it will use that as the initialization vector
    """
    if challenge is None:
        return AES.new(_pad256(key), AES.MODE_ECB)
    else:
        return AES.new(_pad256(key), AES.MODE_CBC, _pad256(challenge))


def encrypt(password, key, challenge=None):
    """Encrypts password with a key and returns the base64 encoded string"""
    ciph = _get_ciph(key, challenge)
    return base64.b64encode(ciph.encrypt(password))


def decrypt(passblob64, key, challenge=None):
    """Decrypts a base64 encoded string with a key"""
    ciph = _get_ciph(key, challenge)
    return ciph.decrypt(base64.b64decode(passblob64))
