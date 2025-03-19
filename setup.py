from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import urllib.request
import json

setup(
    name='clisearch',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        search=search.main:search
    ''',
)
