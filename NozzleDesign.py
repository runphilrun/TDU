"""
Nozzle Design Tool v1.0.0
Philip Linden
7/17/16
"""

import configparser

# set global constants
g0 = 9.81  # Standard gravity [m/s^2]
R = .008314  # Universal gas constant [J/K*kmol]
# load values from config.ini
parser = configparser.ConfigParser()
parser.read('config.ini')
# propellant properties
k = parser.getfloat('Propellant', 'k')  # specific heat ratio
mMol = parser.getfloat('Propellant', 'mMol')  # molecular weight
# nozzle properties
thk = parser.getfloat('Nozzle', 'thk')  # nozzle thickness
rhoNoz = parser.getfloat('Nozzle', 'rhoNoz')  # nozzle density
# chamber properties
Tc = parser.getfloat('Chamber', 'Tc')  # chamber temp
Pc = parser.getfloat('Chamber', 'Pc')  # chamber pressure
