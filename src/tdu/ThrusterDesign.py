"""
Thruster Design Utility v1.0.0
Philip Linden
7/17/16
"""

from configparser import *
from math import *
import numpy as np
import matplotlib.pyplot as plt

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
        self._Rt = (At/(pi))**.5

    @property
    def Ae(self):
        return self._Ae

    @Ae.setter
    def Ae(self, Ae):
        self._Ae = Ae
        self._Re = (Ae/(pi))**.5

    @property
    def Re(self):
        return self._Re
    @Re.setter
    def Re(self,Re):
        self._Re = Re
        self._Ae = pi*(Re**2)

    @property
    def Rt(self):
        return self._Rt
    @Rt.setter
    def Rt(self,Rt):
        self._Rt = Rt
        self._At = pi*(Rt**2)

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

    @property
    def mdot(self):
        return self._mdot
    @mdot.setter
    def mdot(self, mdot):
        self._mdot = mdot

    @property
    def Tt(self):
        return self._Tt
    @Tt.setter
    def Tt(self, Tt):
        self._Tt = Tt

    @property
    def Pt(self):
        return self._Pt
    @Pt.setter
    def Pt(self, Pt):
        self._Pt = Pt

def init():
    """
    :return thruster:
    """
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
    return thruster

def display(thruster):
    """
    :param thruster:
    :return:
    all thruster properties must be set.
    """
    print('-----',
          '\nChamber conditions:'
          '\nk',thruster.prop.k,
          '\nR',thruster.prop.R,'[kJ/kg]',
          '\nTc',thruster.chbr.Tc,'[K]',
          '\nPc',thruster.chbr.Pc,'[bar]')
    print('\nThroat conditions:'
          '\nTt',thruster.Tt,'[K]',
          '\nPt',thruster.Pt,'[bar]',
         '\nAt =',thruster.noz.At,'[m^2]',
          '\nRt =',thruster.noz.Rt*1000,'[mm]')
    print('\nExit conditions:',
          '\ne',thruster.noz.e,
          '\nAe =',thruster.noz.Ae,'[m^2]',
          '\nRe =',thruster.noz.Re*1000,'[mm]',
          '\nL =',thruster.noz.L(),'[m]',
          '\n-----')

def solveMach(nozzle, k):
    """
    :param nozzle:
    :param k:
    :return M:
    solve Mach number from area ratio by iteration. assume supersonic
    https://www.grc.nasa.gov/WWW/winddocs/utilities/b4wind_guide/mach.html
    """
    A = nozzle.Ae
    At = nozzle.At
    P = 2/(k+1)
    Q = 1-P
    E = (k+1)/(k-1)
    R = (A/At)**((2*Q)/P)
    a = Q**(1/P)
    r = (R-1)/(2*a)
    X = 1/((1+r)+sqrt(r*(r+2))) #initial guess
    diff = 1 #initalize iteration difference
    while abs(diff) > .01:
        F = (P*X+Q)**(1/P)-R*X
        dF = (P*X+Q)**((1/P)-1)-R
        Xnew = X- F/dF
        diff = Xnew - X
        X = Xnew
    M = 1/sqrt(X)
    return M

def main():
    thruster = init()
    k = thruster.prop.k
    R = thruster.prop.R
    Tc = thruster.chbr.Tc
    Pc = thruster.chbr.Pc

    # get inputs
    print('Set some initial conditions:')
    thruster.noz.Re = float(input('Nozzle exit radius [mm]: '))/1000
    Ae = thruster.noz.Ae #resolve Ae from Re
    L = float(input('Nozzle length [mm]: '))/1000
#    thruster.noz.e = (float(input('Expansion ratio (Ae/At): ')))

    # throat conditions
    At = pi*(sqrt(thruster.noz.Ae/pi)-2*L*sin(radians(15)))**2
    thruster.noz.At = At
    critP = (2/(k+1))**(k/(k-1))
    thruster.Pt = Pc*critP
    Pt = thruster.Pt
    thruster.Tt = Tc*(2/(k+1))
    Tt = thruster.Tt
    mdot = (Pt/(R*Tt))*sqrt(k*R*Tt)*At

    #exit conditions
    M = solveMach(thruster.noz,k)
    ve = sqrt(((2*k*R*Tc)/(k-1))*(1-(1/(1+((k-1)/2)*M**2))))
    Pe = Pc/((1+((k-1)/2)*M**2)**(k/(k-1)))

    #characteristic values
    vc = Pt*At/mdot
    CF = (ve/vc)+(Ae/At)*(Pe/Pc)

    #performance
    F = At*Pc*CF
    Isp = F/(g0*mdot)

    print('\nDEBUG:',
          '\n At =', At*1000, '[mm]',
          '\n M  =', M,
          '\n ve =', ve, '[m/s]',
          '\n F  =', F, '[N]',
          '\n Isp=', Isp, '[s]'
          )
#    display(thruster)
    return

if __name__ == "__main__":
    main()
