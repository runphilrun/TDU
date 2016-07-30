"""
Thruster Design Utility v1.0.0
Philip Linden
7/17/16
"""

from configparser import *
from math import *


# set global constants
g0 = 9.81  # [m/s^2] Standard gravity
R0 = .008314  # [J/K*kmol] Universal gas constant


class Prop(object):
    def __init__(self, name, k, mMol):
        self.name = name
        self.k = k
        self.mMol = mMol
        self.R = R0 / self.mMol

class Nozzle(object):
    def __init__(self, matl, thk, rho):
        self.matl = matl
        self.thk = thk
        self.rho = rho
        self._e = 1.0

    def emode(self):
        return self._emode

    """
    BUGGY, AREAS ARE DOUBLE DIPPING IN CHECKS/UPDATES.
        def set_emode(self,debug=False):
            default = '1'
            if debug:
                self._emode = default
            else:
                print('Enter number to select mode.')
                option = input('[1] Fixed expansion ratio, At and Ae update each other | '
                               '[2] Fixed At, Ae and expansion ratio update each other | '
                               '[3] Cancel & use default'
                               '\nSelection: ')
                if not (option == '1' or option == '2'):
                    print('Operation cancelled! Mode set to default =',default)
                    option = default
                self._emode = option
    """

    @property
    def e(self):
        return self._e

    @e.setter
    def e(self, e):
        if self._e < 1:
            raise Exception("Expansion ratio must be greater than 1.")
        self._e = e

    def solve_e(self, Ae, At):
        self._e = Ae / At

    @property
    def At(self):
        return self._At

    @At.setter
    def At(self, At):
        self._At = At
        self._Rt = (At/(2*pi))**.5

    @property
    def Ae(self):
        return self._Ae

    @Ae.setter
    def Ae(self, Ae):
        self._Ae = Ae
        self._Re = (Ae/(2*pi))**.5

    @property
    def Re(self):
        return self._Re
    @Re.setter
    def Re(self,Re):
        self._Re = Re
        self._Ae = 2*pi*Re**2

    @property
    def Rt(self):
        return self._Rt
    @Rt.setter
    def Rt(self,Rt):
        self._Rt = Rt
        self._At = 2*pi*Rt**2

    def L(self):
        self._Re = sqrt(self._Ae / pi)
        self._Rt = sqrt(self._At / pi)
        alpha = radians(15)
        return (self._Re - self._Rt) / tan(alpha)

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
    config = ConfigParser()
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
    print('Settings retrieved from config.ini\n------')
    print('Propellant:', prop.name,'','k =',prop.k,'','mMol =',prop.mMol)
    print('Chamber:', chbr.Tc, 'K,', chbr.Pc, 'bar')
    print('Nozzle:', noz.matl, '@', noz.thk, 'm thick')
    print('------')

    # get inputs
    #thruster.noz.set_emode(True) #True for debug ON
    thruster.mdot = float(input('Mass flow rate [kg/s]: '))  # mass flow rate [kg/s]
    thruster.noz.Re = (float(input('Nozzle exit radius [mm]: '))*.001)
    return thruster


def main():
    thruster = init()
    mdot = thruster.mdot
    k = thruster.prop.k
    R = thruster.prop.R
    Tc = thruster.chbr.Tc
    Pc = thruster.chbr.Pc

    # find optimal throat area based on mdot
    thruster.noz.At = (mdot * sqrt(k*R*Tc))/(Pc * k * sqrt((2/(k+1))**((k+1)/(k-1))))
    e = thruster.noz.solve_e(thruster.noz.Ae,thruster.noz.At)

    #display results
    print('-----',
          '\nmdot',mdot,'[kg]',
          '\ne',e,
          '\nk',k,
          '\nR',R,'[kJ/kg]',
          '\nTc',Tc,'[K]',
          '\nPc',Pc,'[bar]')
    print('\nAt =',thruster.noz.At,'[m^2]',
          '\nAe =',thruster.noz.Ae,'[m^2]',
          '\nRt =',thruster.noz.Rt*1000,'[mm]',
          '\nRe =',thruster.noz.Re*1000,'[mm]',
          '\nL =',thruster.noz.L(),'[m]')


    return


if __name__ == "__main__":
    main()
