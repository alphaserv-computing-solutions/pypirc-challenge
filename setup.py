#!/usr/bin/env python
"""
pypirc Challenge

Copyright (C) 2016 AlphaServ Computing Solutions
"""

from setuptools import setup

setup(
    name='pypirc-challenge',
    version='1.0.0',
    description='Python module to provide a challenge instead of a password from .pypirc',
    url='https://github.com/alphaserv-computing-solutions/pypirc-challenge',
    author='Alphadelta14',
    author_email='alpha@alphaservcomputing.solutions',
    license='MIT',
    install_requires=[
        'keyring'
    ],
    entry_points={
        'keyring backends': [
            'pypirc_challenge=pypirc_challenge.ChallengeBackend',
        ]
    },
    packages=['pypirc_challenge'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2'
    ]
)
