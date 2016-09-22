function varargout = tdu % main function
    clear all;
    clc;
    %% universal constants
    universal_gas_constant= 8.3144598; % [J/(mol*K)]
    standard_gravity = 9.81; % [m/s^2]
    unitless='[-]';
    
%%  === EDIT THESE ===
    % gas properties of propellant
    propellant_name = 'Air';
    specific_heat_ratio = 1.4; % 1.4 for air
    molar_mass = .0289645; % .0289645 for air
    molar_mass_units = '[kg/mol]';
    
    % chamber conditions
    chamber_temperature = 273; % 273 K = 0C
    temperature_units = '[K]';
    chamber_pressure = 1.01325; % 1 atm = 101325 Pa
    pressure_units = '[Pa]';
    
    % nozzle geometry
    exit_radius = .014160; % radius at nozzle exit
    throat_radius = .01; % radius at nozzle throat
    length_units = '[m]';
    conical_half_angle = 15; % half angle of conical nozzle, 15 degrees is optimal
    angle_units = '[deg]';
%   ===------------===   

%% Math (the fun part)

%           NOZZLE NOMENCLATURE
%   ********************************
%
%              /-
%             /
%     ===\---/          c = chamber
%     (c) (t)  (e)      t = throat
%     ===/---\          e = exit
%             \
%              \-
%   ********************************

    specific_gas_constant = universal_gas_constant/molar_mass; 
    specific_gas_constant_units = '[J/kg K]';
    exit_area = pi*exit_radius^2; 
    throat_area = pi*throat_radius^2; 
    area_units = '[m^2]';
    length = (exit_radius-throat_radius)/tan(deg2rad(conical_half_angle)); % [m]
    
    %% Throat conditions
    % We are designing a nozzle that "chokes" the fluid flow at the throat,
    % so we assume that at the throat, Mach number is isentropically
    % brought to the boundary between supersonic and subsonic flow (Mach=1)
    throat_temperature = chamber_temperature*(2/(specific_heat_ratio+1)); 
    throat_pressure = chamber_pressure*(2/(specific_heat_ratio+1))^(specific_heat_ratio/(specific_heat_ratio-1)); 
    throat_velocity = sqrt(specific_heat_ratio*specific_gas_constant*throat_temperature);
    % use nozzle areas to find Mach number at the exit via the Newton-Raphson method
    exit_mach = solve_mach(exit_area,throat_area,specific_heat_ratio);
%   since
%       mass_flow_rate = density*speed*cross_sectional_area
%   and from the ideal gas law, PV=RT
    throat_density = throat_pressure/(specific_gas_constant*throat_temperature); %[kg/m^3]
%   and at the throat Mach = 1 so flow rate (speed of flow) is the fluid's speed of sound at the throat
    throat_flowrate = sqrt(specific_heat_ratio*specific_gas_constant*throat_temperature);
    mass_flowrate = throat_density*throat_flowrate*throat_area; 
    mass_flowrate_units = '[kg/s]';

    %% Exit conditions
%   it's much easier to define the flow characteristics at the exit in
%   terms of ratios for now. We'll resolve them into actual useful values
%   later.
%   these are ratios between the throat parameter (numerator) and the exit
%   parameter (denominator). 
%   For example, area_ratio = throat_area/exit_area
 
%(already know this one)    area_ratio = exit_mach(((specific_heat_ratio+1)/2)/(1+(specific_heat_ratio-1)/2*exit_mach^2))^((specific_heat_ratio+1)/(2*(specific_heat_ratio-1)));
    temperature_ratio = 1+((specific_heat_ratio-1)/2)*exit_mach^2;
    pressure_ratio = temperature_ratio^((specific_heat_ratio-1)/specific_heat_ratio);
    
    exit_temperature = chamber_temperature/temperature_ratio; 
    exit_pressure = chamber_pressure/pressure_ratio; 
    
    exit_velocity = sqrt((2*specific_heat_ratio*specific_gas_constant*chamber_temperature)/(specific_heat_ratio-1)*(1-1/(1+(specific_heat_ratio-1)/2*exit_mach^2)));
    velocity_units = '[m/s]';
    
    %% Thrust and Specific Impulse
    thrust = mass_flowrate*exit_velocity + exit_pressure*exit_area;
    force_units = '[N]';
    specific_impulse = thrust/(mass_flowrate*standard_gravity);
    isp_units='[s]';
    
    %% format & display outputs
    linedivider='------------';
    result =  {'Propellant','',propellant_name;
               linedivider,'','';
               'Specific heat ratio', specific_heat_ratio, unitless;
               'Molar mass', molar_mass, molar_mass_units;
               'Specific gas constant',specific_gas_constant,specific_gas_constant_units;
               linedivider,'','';
               'Chamber temperature', chamber_temperature, temperature_units;
               'Chamber pressure', chamber_pressure, pressure_units;
               'Exit radius', exit_radius, length_units;
               'Throat radius', throat_radius, length_units;
               'Half-angle',conical_half_angle, angle_units;
               linedivider,'','';
               'Length',length,length_units;
               'Exit area',exit_area,area_units;
               'Throat area',throat_area,area_units;
               'Throat temperature',throat_temperature,temperature_units;
               'Throat pressure',throat_pressure,pressure_units;
               'Mass flow rate',mass_flowrate,mass_flowrate_units;
               linedivider,'','';
               'Exit temperature',exit_temperature,temperature_units;
               'Exit pressure',exit_pressure,pressure_units;
               linedivider,'','';
               'Exhaust velocity',exit_velocity,velocity_units;
               'Thrust',thrust,force_units;
               'Specific impulse',specific_impulse,isp_units;
               linedivider,'','';
               'Exit Mach',exit_mach,unitless;
               'A/At',exit_area/throat_area,unitless;
               'T/Tc',exit_temperature/chamber_temperature,unitless;
               'P/Pc',exit_pressure/chamber_pressure,unitless;
               'v/at',exit_velocity/throat_velocity,unitless;
               }; 

    display(result);
end

function Mach = solve_mach(A,At,k)
%   solve Mach number from area ratio by Newton-Raphson Method. (assume
%   supersonic)
%   https://www.grc.nasa.gov/WWW/winddocs/utilities/b4wind_guide/mach.html
    P = 2/(k+1);
    Q = 1-P;
    R = (A/At).^((2*Q)/P);
    a = Q.^(1/P);
    r = (R-1)/(2*a);
    X = 1/((1+r)+sqrt(r*(r+2)));  % initial guess
    diff = 1;  % initalize termination criteria
    while abs(diff) > .0001
        F = (P*X+Q).^(1/P)-R*X;
        dF = (P*X+Q).^((1/P)-1)-R;
        Xnew = X - F/dF;
        diff = Xnew - X;
        X = Xnew;
    end
    Mach = 1/sqrt(X);
end

function display(result)
    [n,~]=size(result);
    for i = 1:n 
        fprintf('\n%24s\t%12f\t%s',result{i,:});
    end
end
