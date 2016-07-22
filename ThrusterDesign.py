"""
Thruster Design Tool v1.0.0
Philip Linden
7/17/16
"""

import configparser
import math

# set global constants
global g0
global R0
g0 = 9.81  # [m/s^2] Standard gravity
R0 = .008314  # [J/K*kmol] Universal gas constant


class Prop(object):
    def __init__(self, name, k, mMol):
        self.name = name
        self.k = k
        self.mMol = mMol

    def gasconstant(self):
        return R0 / self.mMol


class Nozzle(object):
    def __init__(self, matl, thk, rho):
        self.matl = matl
        self.thk = thk
        self.rho = rho
        self._e = 1

    @property
    def e(self):
        return self._e

    @e.setter
    def e(self, e):
        if self._e < 1:
            raise Exception("Expansion ratio must be greater than 1.")
        self._e = e

    def set_e(self, Ae, At):
        self._e = Ae / At

    @property
    def At(self):
        if self._At == 0:
            raise Exception("Throat area not set. Set At or define Ae & e.")
        self._At = self._Ae / self._e
        return self._At

    @At.setter
    def At(self, At):
        self._At = At
        self._Ae = self._At * self._e

    @property
    def Ae(self):
        if self._Ae == 0:
            raise Exception("Exit area not set. Set Ae or define At & e.")
        else:
            self._Ae = self._At * self._e
            return self._Ae

    @Ae.setter
    def Ae(self, Ae):
        self._Ae = Ae
        self._At = self._Ae / self._e

    def h(self):
        Re = math.sqrt(self.Ae / math.pi)
        Rt = math.sqrt(self.At / math.pi)
        alpha = math.radians(15)
        return Re / math.tan(alpha) - Rt / math.tan(alpha)


class Chamber(object):
    def __init__(self, Tc, Pc):
        self.Tc = Tc
        self.Pc = Pc


class Thruster(object):
    def __init__(self, prop, noz, chbr):
        self.prop = prop
        self.noz = noz
        self.chbr = chbr
        self.mdot = 0

    @property
    def mdot(self):
        return self._mdot
    @mdot.setter
    def mdot(self, mdot):
        self._mdot = mdot

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
    thruster = Thruster(
        prop,
        noz,
        chbr
    )
    # print summary
    print('Propellant:', prop.name)
    print('Chamber:', chbr.Tc, 'K,', chbr.Pc, 'bar')
    print('Nozzle:', noz.matl, '@', noz.thk, 'm thick')

    # get inputs
    thruster.mdot = float(input('Mass flow rate [kg/s]: '))  # mass flow rate [kg/s]

    return thruster


def main():
    thruster = init()
    noz = thruster.noz
    noz.e = 2 # set expansion ratio
    noz.At = .02 # set throat area
    noz.Ae = 10 # set exit area -> throat area changes to maintain e
    noz.e = 500 # set new expansion ratio -> At and Ae
    noz.set_e(500,250)
    print('debug:', noz.At, noz.e, thruster.mdot, thruster.noz.Ae,noz.e == 2)

    print('Restructure so that At remains fixed at its set value \n'
          'e is varied as the controlled value (for graphs, etc) \n'
          'and Ae is derived from At * e. \n\n'
          'Since At is determined by mass flow rate and prop, this is \n'
          'acceptable.')
    return


if __name__ == "__main__":
    main()
