#!/usr/bin/env python
from os import path
from codecs import open
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'tdu',
    version = '0.0.1',
    description = 'Thruster design utility.',
    long_description = long_description,
    url = 'https://github.com/runphilrun/tdu',
    author = 'Phil-Linden',
    author_email = 'pjl7651@rit.edu',
    license = 'Apache-2.0',
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords = '',
    package_dir = {'': 'src'},
    packages = find_packages('src'),
    entry_points = {
        'console_scripts': [
            'tdu = tdu.cli:main'
        ]
    }
)
