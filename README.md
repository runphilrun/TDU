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
### Matlab
Open `Matlab/tdu.m` in Matlab 2014 or newer.
Edit fields as indicated to specify the propellant gas properties and nozzle dimensions of the engine, then run the script.
Mach number, temperature ratio, and pressure ratio at the exit of the nozzle agree with [NASA Report 1135](http://www.nasa.gov/sites/default/files/734673main_Equations-Tables-Charts-CompressibleFlow-Report-1135.pdf) for air at 1 atm with an area ratio of 2.005.

### Python

```bash
$ pip install tdu
$ tdu --help
```
Set propellant gas properties, nozzle geometry and chamber conditions in `config.ini`.

Run `tdu.py`.

## About & Documentation
Please refer to the [STEMN project page](http://stemn.com/projects/thruster-design-tool) for detailed information about the project and general theory.

> *If you encounter any bugs, please report them in the [Issue Tracker](https://github.com/runphilrun/ThrusterDesign/issues)!*
