#!/usr/bin/env python
"""Holds project dependencies and metadata."""

from setuptools import find_packages, setup

setup(
    name='overcooked_ai',
    version='0.0.1',
    description='Cooperative multi-agent environment based on Overcooked',
    author=('Micah Carroll<mdc@berkeley.edu>, Matt Fontaine<mfontain@usc.edu>, '
            'Stefanos Nikolaidis<nikolaid@usc.edu>, '
            'Yulun Zhang<yulunzha@usc.edu>, Bryon Tjanaka<tjanaka@usc.edu>'),
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tqdm',
        'gym',
        'pygame',
        'pandas',
    ])
