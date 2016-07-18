"""
Nozzle Design Tool v1.0.0
Philip Linden
7/17/16
"""

import configparser
import math

# set global constants
g0 = 9.81  # Standard gravity [m/s^2]
R0 = .008314  # Universal gas constant [J/K*kmol]
# load values from config.ini
parser = configparser.ConfigParser()
parser.read('config.ini')
# propellant properties
propName = parser.get('Propellant', 'name')  # prop name
k = parser.getfloat('Propellant', 'k')  # specific heat ratio
mMol = parser.getfloat('Propellant', 'mMol')  # molecular weight
# nozzle properties
nozMatl = parser.get('Nozzle', 'matl')  # nozzle material name
thk = parser.getfloat('Nozzle', 'thk')  # nozzle thickness
rhoNoz = parser.getfloat('Nozzle', 'rhoNoz')  # nozzle density
# chamber properties
Tc = parser.getfloat('Chamber', 'Tc')  # chamber temp
Pc = parser.getfloat('Chamber', 'Pc')  # chamber pressure

# print summary
print('Propellant:', propName)
print('Chamber:', Tc, 'K,', Pc, 'bar')
print('Nozzle:', nozMatl, '@', thk, 'm thickness')

# get inputs
mdot = float(input('Mass flow rate [kg/s]: '))  # mass flow rate [kg/s]
maxD = float(input('Max nozzle exit diameter [cm]: '))
maxAe = math.pi*pow(2, .5*maxD/100)  # max exit area [m]
