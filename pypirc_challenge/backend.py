"""pypirc Challenge keyring Backend

>>> import keyring
>>> from pypirc_challenge import ChallengeBackend
>>> keyring.set_keyring(ChallengeBackend())
>>> keyring.get_password('service', 'username')
'password'
>>>

"""

import keyring


class ChallengeBackend(keyring.backend.KeyringBackend):
    """pypirc Challenge keyring Backend
    """
    pass
