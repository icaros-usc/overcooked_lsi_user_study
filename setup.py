#!/usr/bin/env python
"""Holds project dependencies and metadata."""

from setuptools import find_packages, setup

setup(
    name='overcooked_ai_user_study',
    version='0.0.0',
    description='User-study data for Overcooked-AI-PCG',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'tqdm',
        'gym',
        'pygame',
        'pandas',
    ])
