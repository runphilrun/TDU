#!/usr/bin/env python
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='thruster-designer',
    version='0.0.1',
    description='Thruster nozzle design tool written.',
    long_description=long_description,
    url='https://github.com/runphilrun/ThrusterDesign',
    author='Phil-Linden',
    author_email='pjl7651@rit.edu',
    license='Apache-2.0',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        "Topic :: Utilities",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3 :: Only'
    ],

    keywords='',

    packages=[],
    setup_requires=['pytest-runner', 'check-manifest'],
    tests_require=['pytest', 'coverage'],

    entry_points={
        'console_scripts': [
            'thruster-designer=thruster_designer:main',
        ],
    },
    test_suite='tests.test_suite'
)
