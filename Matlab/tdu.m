function varargout = tdu % main function
    %% universal constants
    universal_gas_constant= 8.3144598 % [J/(mol*K)]
    standard_gravity = 9.81 % [m/s^2]
    
%%  === EDIT THESE ===
    % gas properties of propellant
    specific_heat_ratio = 1.4 % 1.4 for air
    molar_mass = .0289645; % [kg/mol]
    
    % chamber conditions
    chamber_temperature = 273; % [K]
    chamber_pressure = 1; % [atm]
    
    % nozzle geometry
    exit_radius = .025; %[m] radius at nozzle exit
    length = .05; %[m] permissible length of nozzle, throat to exit
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

    specific_gas_constant = universal_gas_constant/molar_mass; %[J/kgK]
    exit_area = pi*exit_radius^2; % [m^2]

    %% Throat conditions
    % at the throat, assume choked flow (M=1) and apply the equation
    %   A_throat/A_exit =
    %       Mach*(((specific_heat_ratio+1)/2)/(1+((specific_heat_ratio -
    %       1)/2)*Mach^2))^((specific_heat_ratio+1)/(2*(specific_heat_ratio-1)))
    throat_area = exit_area*(((specific_heat_ratio+1)/2)/(1+((specific_heat_ratio - 1)/2)))^((specific_heat_ratio+1)/(2*(specific_heat_ratio-1))); %[m^2]
    throat_radius = sqrt(throat_area/pi); % [m]
    conical_half_angle = atan((exit_radius-throat_radius)/length); % [radians]
    
    % similarly, assuming isentropic and choked flow
    throat_temperature = chamber_temperature*(2/(specific_heat_ratio+1));
    throat_pressure = chamber_pressuure*(2/(specific_heat_ratio+1))^(specific_heat_ratio/(specific_heat_ratio-1));
    
    % use nozzle areas to find Mach number at the exit via the Newton-Raphson method
    exit_mach = solve_mach(exit_area,1,1.4);
%   since
%       mass_flow_rate = density*speed*cross_sectional_area
%   and from the ideal gas law, PV=RT
    throat_density = throat_pressure/(specific_gas_constant*throat_temperature);
%   and at the throat Mach = 1 so flow rate (speed of flow) is the fluid's speed of sound at the throat
    throat_flowrate = sqrt(specific_heat_ratio*specific_gas_constant*throat_temperature);
    mass_flowrate = throat_density*throat_flowrate*throat_area;

    %% Exit conditions
%   it's much easier to define the flow characteristics at the exit in
%   terms of ratios for now. We'll resolve them into actual useful values
%   later.
%   these are ratios between the throat parameter (numerator) and the exit
%   parameter (denominator). 
%   For example, area_ratio = throat_area/exit_area

    area_ratio = exit_mach(((specific_heat_ratio+1)/2)/(1+(specific_heat_ratio-1)/2*exit_mach^2))^((specific_heat_ratio+1)/(2*(specific_heat_ratio-1)));
    temperature_ratio = 1+(specific_heat_ratio-1)/2*exit_mach^2;
    pressure_ratio = temperature_ratio^((specific_heat_ratio-1)/specific_heat_ratio);
    
    
end

function Mach = solve_mach(A,A_throat,specific_heat_ratio)
%   solve Mach number from area ratio by Newton-Raphson Method. (assume
%   supersonic)
%   https://www.grc.nasa.gov/WWW/winddocs/utilities/b4wind_guide/mach.html
    
    % establish shorthand
    At = A_throat;
    k = specific_heat_ratio;

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