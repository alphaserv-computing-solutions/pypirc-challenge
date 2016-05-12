"""pypirc Challenge keyring Backend

>>> import keyring
>>> from pypirc_challenge import ChallengeBackend
>>> keyring.set_keyring(ChallengeBackend())
>>> keyring.get_password('service', 'username')
'password'
>>>

"""

import contextlib
import os

import keyring
from six.moves import configparser, urllib

from pypirc_challenge import encrypt, decrypt


class RequestMethodCompat(urllib.request.Request):
    """Ensure that requests have a settable method"""
    def __init__(self, *args, **kwargs):
        method = kwargs.pop('method', None)
        urllib.request.Request.__init__(self, *args, **kwargs)
        self.method = method

    def get_method(self):
        """Gets the method of this Request. This shims Python 2's urllib
        """
        if self.method is not None:
            return self.method
        if self.has_data():
            return 'POST'
        return 'GET'


@contextlib.contextmanager
def null_context():
    """Returns an empty context"""
    yield


class ChallengeBackend(keyring.backend.KeyringBackend):
    """pypirc Challenge keyring Backend
    """
    priority = 2

    def _read_pypirc(self):
        """Reads the pypirc into a ConfigParser

        Raises an IOError if the config file does not exist
        """
        config = configparser.ConfigParser({
            'key': 'VdkS58HE4v4sGhtZAQRkJGMkZsq17pCx',
            'passuri': 'file://'+os.path.join(os.path.expanduser('~'), '.pypipass')
        })
        config.read(os.path.join(os.path.expanduser('~'), '.pypirc'))
        return config

    def _open_passuri(self, passuri, data=None, method='GET'):
        """Reads a passblob URI from the configuration into a request handle

        For file:// protocol, this adds support for PUT and DELETE
        """
        _ = self
        req = RequestMethodCompat(url=passuri, data=data, method=method)
        if req.get_type() == 'file':
            if req.get_method() == 'PUT':
                with open(req.get_selector(), 'w') as handle:
                    handle.write(data)
                return null_context
            elif req.get_method() == 'DELETE':
                os.unlink(req.get_selector())
                return null_context
        return urllib.request.urlopen(req)

    def set_password(self, servicename, username, password):
        """Sets a password if supported by remote

        Performs an HTTP PUT with the body being the b64 encrypted password
        If the passuri is a file://, this will overwrite its contents
        """
        config = self._read_pypirc()
        config_user = config.get(servicename, 'username')
        if config_user != username:
            raise ValueError('Setting password only works for user: {}'.format(config_user))
        key = config.get(servicename, 'key')
        with self._open_passuri(config.get(servicename, 'passuri'),
                                data=encrypt(password, key),
                                method='PUT'):
            pass

    def get_password(self, servicename, username):
        """Gets a password

        Performs an HTTP GET
        """
        try:
            config = self._read_pypirc()
        except IOError:
            return None
        config_user = config.get(servicename, 'username')
        if config_user != username:
            raise ValueError('Getting password only works for user: {}'.format(config_user))
        key = config.get(servicename, 'key')
        with self._open_passuri(config.get(servicename, 'passuri')) as handle:
            passblob = handle.read()
        return decrypt(passblob, key)

    def delete_password(self, servicename, username, password):
        """Sets a password if supported by remote

        Performs an HTTP DELETE
        If the passuri is a file://, this will delete it
        """
        try:
            config = self._read_pypirc()
        except IOError:
            return
        with self._open_passuri(config.get(servicename, 'passuri'), method='DELETE'):
            pass
