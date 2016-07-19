"""
Nozzle Design Tool v1.0.0
Philip Linden
7/17/16
"""

import configparser
import math

# set global constants
global g0
global R0
g0 = 9.81       # [m/s^2] Standard gravity
R0 = .008314    # [J/K*kmol] Universal gas constant


class Prop(object):
    def __init__(self, name, k, mMol):
        self.name = name
        self.k = k
        self.mMol = mMol

    def gasconstant(self):
        return R0/self.mMol


class Nozzle(object):
    def __init__(self, matl, thk, rho):
            self.matl = matl
            self.thk = thk
            self.rho = rho

    @property
    def e(self):
        return self._e

    @e.setter
    def e(self, e):
        if e < 1:
            raise Exception("Expansion ratio must be greater than 1")
        else:
            self._e = e

    @property
    def At(self):
        return self._At

    @At.setter
    def At(self, val):
        self._At = val

    def Ae(self):
        if self.At*self.e > .1:
            raise Exception("Exit area larger than 10 cm")
        else:
            return self.At*self.e

    @property
    def h(self):
        Re = math.sqrt(self.Ae / math.pi)
        Rt = math.sqrt(self.At / math.pi)
        alpha = math.radians(15)
        return Re / math.tan(alpha) - Rt / math.tan(alpha)


class Chamber(object):
    def __init__(self, Tc, Pc):
        self.Tc = Tc
        self.Pc = Pc


def init():
    config = configparser.ConfigParser()
    config.read('config.ini')
    prop = Prop(
        config.get('Prop', 'name'),
        config.getfloat('Prop', 'k'),
        config.getfloat('Prop', 'mMol'),
    )
    noz = Nozzle(
        config.get('Nozzle', 'matl'),
        config.getfloat('Nozzle', 'thk'),
        config.getfloat('Nozzle', 'rho')
    )
    chbr = Chamber(
        config.getfloat('Chamber', 'Tc'),
        config.getfloat('Chamber', 'Pc'),
    )
    # print summary
    print('Propellant:', prop.name)
    print('Chamber:', chbr.Tc, 'K,', chbr.Pc, 'bar')
    print('Nozzle:', noz.matl, '@', noz.thk, 'm thick')

    # get inputs
    mdot = float(input('Mass flow rate [kg/s]: '))  # mass flow rate [kg/s]

    return prop, noz, chbr


def main():
    prop, noz, chbr = init()
    noz.At = .02
    noz.e = 1.5
    print(noz.At, noz.e, noz.Ae)
    return

if __name__ == "__main__":
    main()