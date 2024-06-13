#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup as __setup__, find_packages

def setup(name='_', install_requires=[]):
    __setup__(
        name=name,
        install_requires=install_requires,
        packages=find_packages(),
    )
