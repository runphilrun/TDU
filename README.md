# Thruster Design Utility
[![Documentation Status](https://readthedocs.org/projects/thrusterdesign/badge/?version=latest)](http://thrusterdesign.readthedocs.io/en/latest/?badge=latest)
[![Build status](https://travis-ci.org/runphilrun/TDU.svg?style=flat-square)](https://travis-ci.org/runphilrun/TDU)
[![GitHub issues](https://img.shields.io/github/issues/runphilrun/TDU.svg)](https://github.com/runphilrun/TDU/issues)
[![PyPI](https://img.shields.io/pypi/v/tdu.svg?style=flat-square)](https://pypi.python.org/pypi/tdu)
[![GitHub stars](https://img.shields.io/github/stars/runphilrun/TDU.svg)](https://github.com/runphilrun/TDU/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/runphilrun/TDU.svg)](https://github.com/runphilrun/TDU/network)
[![GitHub license](https://img.shields.io/badge/license-Apache%202-blue.svg)](https://raw.githubusercontent.com/runphilrun/TDU/master/LICENSE.md)


> Tool to aid in design of small monopropellant thrusters. *[View this project on STEMN](http://stemn.com/projects/thruster-design-tool)*

## Abstract
The thruster's nozzle, propellant, and chamber conditions each have a huge impact on performance. The fluid mechanics that model engine effectiveness are pretty complicated, unfortunately. The purpose of this script is to make it easy to see how tweaks in nozzle geometry, propellants, and chamber conditions affect performance in order to find the optimal design solution.

## Features
* Simulate the performance of a thruster in space for a given set of parameters and output performance metrics.
* Output simulation data in a useful manner.
* Allow the user to easily tweak parameters.

## Usage
```bash
$ pip install tdu
$ tdu --help
```
Run `ThrusterDesign.py` and input parameters when prompted.

## About & Documentation
Please refer to the [STEMN project page](http://stemn.com/projects/thruster-design-tool) for detailed information about the project and general theory.

> *If you encounter any bugs, please report them in the [Issue Tracker](https://github.com/runphilrun/ThrusterDesign/issues)!*
