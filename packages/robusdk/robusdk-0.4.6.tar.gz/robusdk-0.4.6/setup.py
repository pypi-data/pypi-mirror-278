#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import setup, find_packages

setup(
    name='robusdk',
    version='0.4.6',
    long_description=(Path(__file__).parent / 'readme.md').read_text(),
    long_description_content_type='text/markdown',
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
