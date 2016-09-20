"""
Thruster Design Utility v1.0.0
Philip Linden
7/17/16
"""

from math import sqrt, pi, radians, tan, sin
from configparser import ConfigParser

# set global constants
g0 = 9.81  # [m/s^2] Standard gravity
R0 = .008314  # [J/K*kmol] Universal gas constant

class Thruster(object):
    def __init__(self, name, k, mMol, matl, thk, rho, Tc, Pc):
        self.name = name
        self.k = k
        self.mMol = mMol
        self.R = R0 / self.mMol
        self.matl = matl
        self.thk = thk
        self.rho = rho
        self._e = 1.0
        self.Tc = Tc
        self.Pc = Pc

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
    def Re(self, Re):
        self._Re = Re
        self._Ae = pi*(Re**2)

    @property
    def Rt(self):
        return self._Rt

    @Rt.setter
    def Rt(self, Rt):
        self._Rt = Rt
        self._At = pi*(Rt**2)

    @property
    def L(self):
        return self._L

    @L.setter
    def L(self, L):
        self._L = L

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

    @property
    def M(self):
        return self._M

    @M.setter
    def M(self, M):
        self._M = M

    @property
    def ve(self):
        return self._ve

    @ve.setter
    def ve(self, ve):
        self._ve = ve

    @property
    def F(self):
        return self._F

    @F.setter
    def F(self, F):
        self._F = F

    @property
    def Isp(self):
        return self._Isp

    @Isp.setter
    def Isp(self, Isp):
        self._Isp = Isp

    @property
    def vc(self):
        return self._vc

    @vc.setter
    def vc(self, vc):
        self._vc =vc

    @property
    def CF(self):
        return self._CF

    @CF.setter
    def CF(self, CF):
        self._CF = CF

def init():
    config = ConfigParser()
    config.read('config.ini')
    thruster = Thruster(
        config.get('Prop', 'name'),
        config.getfloat('Prop', 'k'),
        config.getfloat('Prop', 'mMol'),
        config.get('Nozzle', 'matl'),
        config.getfloat('Nozzle', 'thk'),
        config.getfloat('Nozzle', 'rho'),
        config.getfloat('Chamber', 'Tc'),
        config.getfloat('Chamber', 'Pc')
    )
    # print summary
    print('Settings retrieved from config.ini\n------')
    print('Propellant:', thruster.name, '', 'k =', thruster.k, '', 'mMol =', thruster.mMol)
    print('Chamber:', thruster.Tc, 'K,', thruster.Pc, 'bar')
    print('Nozzle:', thruster.matl, '@', thruster.thk, 'm thick')
    print('------')
    return thruster

def display(thruster):
    print('-----',
          '\nChamber conditions:'
          '\nk  =', thruster.k,
          '\nR  =', thruster.R, '[kJ/kg]',
          '\nTc =', thruster.Tc, '[K]',
          '\nPc =', thruster.Pc, '[bar]')
    print('\nThroat conditions:'
          '\nRt =', thruster.Rt*1000, '[mm]',
          '\nAt =', thruster.At, '[m^2]',
          '\nTt =', thruster.Tt, '[K]',
          '\nPt =', thruster.Pt, '[bar]')
    print('\nExit conditions:',
          '\ne  =', thruster.e,
          '\nAe =', thruster.Ae, '[m^2]',
          '\nRe =', thruster.Re*1000, '[mm]',
          '\nL  =', thruster.L, '[m]',
          '\nmdot', thruster.mdot, '[kg/s]',
          '\nMe =', thruster.M,
          '\nve =', thruster.ve, '[m/s]',
          '\nF  =', thruster.F, '[N]',
          '\nIsp=', thruster.Isp, '[s]')
    print('\nCharacteristic Values:',
          '\nvc =', thruster.vc,
          '\nCF =', thruster.CF,
          '\n-----')

def solveMach(nozzle, k):
    """
    solve Mach number from area ratio by iteration. assume supersonic
    https://www.grc.nasa.gov/WWW/winddocs/utilities/b4wind_guide/mach.html
    """
    A = nozzle.Ae
    At = nozzle.At
    P = 2/(k+1)
    Q = 1-P
    # E = (k+1)/(k-1)
    R = (A/At)**((2*Q)/P)
    a = Q**(1/P)
    r = (R-1)/(2*a)
    X = 1/((1+r)+sqrt(r*(r+2)))  # initial guess
    diff = 1  # initalize iteration difference
    while abs(diff) > .01:
        F = (P*X+Q)**(1/P)-R*X
        dF = (P*X+Q)**((1/P)-1)-R
        Xnew = X - F/dF
        diff = Xnew - X
        X = Xnew
    M = 1/sqrt(X)
    return M

def main():
    thruster = init()
    # retrieve constants
    k = thruster.k
    R = thruster.R
    Tc = thruster.Tc
    Pc = thruster.Pc

    # get inputs
    print('Set some initial conditions:')
    thruster.Re = float(input('Nozzle exit radius [mm]: '))/1000
    Ae = thruster.Ae  # resolve Ae from Re
#    L = float(input('Nozzle length [mm]: '))/1000
    thruster.Rt = float(input('Nozzle throat radius [mm]: '))/1000
    At = thruster.At
    L = (thruster.Re-thruster.Rt)/sin(radians(15))
    thruster.L = L

    # throat conditions
    Tt = Tc*(2/(k+1))
	Pt = Pc*(2/(k+1))**(k/(k-1))
    throatDensity=Pt/(R*Tt)
	vt = sqrt(k*R*Tt)
	mdot=throatDensity*vt*At

    thruster.At = At
    thruster.Pt = Pt
    thruster.Tt = Tt
    thruster.mdot = mdot

    # exit conditions
    M = solveMach(thruster, k)
    ve = sqrt(((2*k*R*Tc)/(k-1))*(1-(1/(1+((k-1)/2)*M**2))))
	tempRatio = 1+((k-1)/2)*M**2
	presRatio = tempRatio**((k-1)/k)
	Te = Tc/tempRatio
    Pe = Pc/presRatio

    thruster.M = M
    thruster.ve = ve
    thruster.Pe = Pe

    # characteristic values
    vc = Pt*At/mdot
    CF = (ve/vc)+(Ae/At)*(Pe/Pc)

    thruster.vc = vc
    thruster.CF = CF

    # performance
    F = mdot*ve+Pe*Ae
    Isp = F/(g0*mdot)

    thruster.F = F
    thruster.Isp = Isp

    display(thruster)
    return

if __name__ == "__main__":
    main()
