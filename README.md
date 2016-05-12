# pypirc-challenge
Python module to provide a challenge instead of a password from .pypirc

## Installation
`python setup.py install`

## Usage
### Setuptools
Once installed, it will automatically be used with setuptool's upload if no
password is provided in your .pypirc file.

`python setup.py sdist upload -r my-server`

### Other
This is a backend that can be provided to the keyring package.

```python
>>> import keyring
>>> from pypirc_challenge import ChallengeBackend
>>> keyring.set_keyring(ChallengeBackend())
>>> keyring.set_password('service', 'username', 'password')
>>> keyring.get_password('service', 'username')
'password'
```

## Configuration
Configuration is stored in `~/.pypirc` under a server section.

```ini
[my-server]
username=myuser
key=sorta secure key
passuri=file:///opt/secure/pypikey
```

### Password URIs
The passuri supports the few basic protocols: http://, ftp://, and file://.

If requesting from a remote server, you can provide `{challenge}` in the url
to set the initialization vector (secures transport). Example:
`http://192.168.1.101:8080/keyserv/pypi?challenge={challenge}`

If you are going to make use of the `set_password` and `delete_password` API,
you must ensure that the remote endpoint has `PUT` and `DELETE` support,
respectively.

## Security Concerns
This should not be relied on for heavily secure applications. This is just slightly
better than storing passwords in plaintext. To maximize security, remove non-owner
read permissions on your .pypirc file and encrypted password file. If serving
the file remotely, provide a challenge and use HTTPS.
