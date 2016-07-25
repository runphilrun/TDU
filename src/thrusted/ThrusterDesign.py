"""
Thruster Design Tool v1.0.0
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
        self.R = float(R0 / self.mMol)

class Nozzle(object):
    def __init__(self, matl, thk, rho):
        self.matl = matl
        self.thk = thk
        self.rho = rho
        self.e = 1.0

    def emode(self):
        return self._emode

    def set_emode(self,debug=False):
        """ Desired feature: add option here to run using e that is defined from
            given Ae and At values
        """
        default = '2'
        if debug == True:
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
        if not (self._At > 0):
            raise Exception("Throat area not set. Set At or define Ae & e.")
        return self._At

    @At.setter
    def At(self, At):
        if self._emode == '1':
            self._At = At
            self.Ae = self._At * self.e
        elif self._emode == '2':
            self._At = At
            self._e = self.Ae / self.Ae

    @property
    def Ae(self):
        if self._Ae <= 0.0:
            raise Exception("Exit area not set. Set Ae or define At & e.")
        else:
            self._Ae = self.At * self.e
            return self._Ae

    @Ae.setter
    def Ae(self, Ae):

        if self._emode == '1':
            self._Ae = Ae
            self._At = self._Ae / self._e
        elif self._emode == '2':
            self._Ae = Ae
            self._e = self._Ae / self._At

    def L(self):
        Re = sqrt(self._Ae / pi)
        Rt = sqrt(self._At / pi)
        alpha = radians(15)
        return Re / tan(alpha) - Rt / tan(alpha)


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
    thruster.noz.set_emode(True) #True for debug ON
    thruster.mdot = float(input('Mass flow rate [kg/s]: '))  # mass flow rate [kg/s]

    return thruster


def main():
    thruster = init()
    mdot = thruster.mdot
    k = thruster.prop.k
    R = thruster.prop.R
    Tc = thruster.chbr.Tc
    Pc = thruster.chbr.Pc
    print('-----','\nmdot',mdot,'\nk',k,'\nR',R,'\nTc',Tc,'\nPc',Pc)
    # find optimal throat area based on mdot
    thruster.noz.At = (mdot * sqrt(k*R*Tc))/(Pc * k * sqrt((2/(k+1))**((k+1)/(k-1))))
    print('At =',thruster.noz.At)
    return


if __name__ == "__main__":
    main()