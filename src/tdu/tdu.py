"""
Thruster Design Utility v2
Philip Linden
10/13/16
"""

from math import sqrt, pi, radians, tan, sin
from configparser import ConfigParser

# set global constants
g0 = 9.81  # [m/s^2] Standard gravity
R0 = 8.314  # [J/mol*K] Universal gas constant

def solveMach(A, At, k):
    """
    solve Mach number from area ratio by iteration. assume supersonic
    https://www.grc.nasa.gov/WWW/winddocs/utilities/b4wind_guide/mach.html
    """
    P = 2/(k+1)
    Q = 1-P
    # E = (k+1)/(k-1)
    R = (A/At)**((2*Q)/P)
    a = Q**(1/P)
    r = (R-1)/(2*a)
    X = 1/((1+r)+sqrt(r*(r+2)))  # initial guess
    diff = 1  # initalize iteration difference
    while abs(diff) > .001:
        F = (P*X+Q)**(1/P)-R*X
        dF = (P*X+Q)**((1/P)-1)-R
        Xnew = X - F/dF
        diff = Xnew - X
        X = Xnew
    M = 1/sqrt(X)
    return M

def main():
    config = ConfigParser()
    config.read('config.ini')
    propType = config.get('Prop', 'name')
    k = config.getfloat('Prop', 'k')
    MW = config.getfloat('Prop', 'MW')
    Re = config.getfloat('Nozzle', 'Re')
    Rt = config.getfloat('Nozzle', 'Rt')
    alpha = radians(config.getfloat('Nozzle','alpha'))
    Tc = config.getfloat('Chamber', 'Tc')
    Pc = config.getfloat('Chamber', 'Pc')
    # print summary
    print('Settings retrieved from config.ini\n------')
    print('Propellant:', propType, '', 'k =', k, '', 'MW =', MW)
    print('Chamber:', Tc, 'K,', Pc, 'Pa')
    print('------')

    R = R0 / MW
    L = (Re-Rt)/sin(alpha)
    Ae = pi*Re**2
    At = pi*Rt**2
    e = Ae/At

    # throat conditions
    Tt = Tc*(2/(k+1))
    Pt = Pc*(2/(k+1))**(k/(k-1))
    throatDensity=Pt/(R*Tt)
    vt = sqrt(k*R*Tt)
    mdot=throatDensity*vt*At

    # exit conditions
    M = solveMach(Ae, At, k)
    ve = sqrt(((2*k*R*Tc)/(k-1))*(1-(1/(1+((k-1)/2)*M**2))))
    tempRatio = 1+((k-1)/2)*M**2
    presRatio = tempRatio**((k-1)/k)
    Te = Tc/tempRatio
    Pe = Pc/presRatio

    # characteristic values
    vc = Pt*At/mdot
    CF = (ve/vc)+(Ae/At)*(Pe/Pc)

    # performance
    F = mdot*ve+Pe*Ae
    Isp = F/(g0*mdot)

    print('-----',
          '\nChamber conditions:'
          '\nk  =', k,
          '\nR  =', R, '[kJ/kg]',
          '\nTc =', Tc, '[K]',
          '\nPc =', Pc, 'Pa')
    print('\nThroat conditions:'
          '\nRt =', Rt, '[m]',
          '\nAt =', At, '[m^2]',
          '\nTt =', Tt, '[K]',
          '\nPt =', Pt, '[bar]')
    print('\nExit conditions:',
          '\ne  =', e,
          '\nAe =', Ae, '[m^2]',
          '\nRe =', Re, '[m]',
          '\nL  =', L, '[m]',
          '\nmdot', mdot, '[kg/s]',
          '\nMe =', M,
          '\nve =', ve, '[m/s]',
          '\nF  =', F, '[N]',
          '\nIsp=', Isp, '[s]')
    print('\nCharacteristic Values:',
          '\nvc =', vc,
          '\nCF =', CF,
          '\n-----')
    return

if __name__ == "__main__":
    main()
