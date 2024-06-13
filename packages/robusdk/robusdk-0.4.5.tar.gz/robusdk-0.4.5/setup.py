#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages

NAME = 'robusdk'

setup(
    name=NAME,
    version='0.4.5',
    packages=find_packages(),
    install_requires=[
        'aiostream',
        'broadcaster',
        'dacite',
        'cbor2',
        'httpx',
        'httpx-ws',
        'kaitaistruct',
    ]
)
