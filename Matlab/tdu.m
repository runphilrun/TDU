function varargout = tdu % main function
    clc;
    close all
    format long
    
    filein = 'sample.tdu'; % input file
    
    % universal constants
    R_0 = 8.3144598; % [J/(mol*K)] universal gas constant
    g_0 = 9.81; % [m/s^2] standard gravity
    unitless='[-]';
    global debug;
    debug = true;
%   === THRUSTER PARAMETERS ===
    % IMPORT FROM FILE
    fid  = fopen(filein,'r');
    if debug;fprintf('reading data from input file (%s)...\n',filein);end
    prop_name   = fscanf(fid,'%s',[1,1]); % descriptive header (no quotes, no spaces)
        if debug;fprintf('\tPropellant:\t\t%8s\n',prop_name);end
    prop_params = fscanf(fid,'%g',[1 2]); % scan propellant parameters
        k           = prop_params(1,1); % specific heat ratio
        mw          = prop_params(1,2); % molecular weight
        if debug;fprintf('\tk:\t\t%16g\n\tmw:\t\t%16g\n',k,mw);end
    total_params= fscanf(fid,'%g',[1 2]); % scan total/stagnation parameters
        T_0         = total_params(1,1); % total temperature
        P_0         = total_params(1,2); % total pressure
        if debug;fprintf('\tT_0:\t%16g\n\tP_0:\t%16g\n',T_0,P_0);end
    geom_size     = fscanf(fid,'%g',[1 1]); % number of geometry nodes
    xcoord = zeros(geom_size,1); radius = zeros(geom_size,1);
        for i=1:geom_size
            geom   = fscanf(fid,'%g',[1 2]);
            xcoord(i)   = geom(1,1); % x coordinate of geometry node
            radius(i)   = geom(1,2); % radius at xcoord
        end
        if debug
            fprintf('\tinlet radius:\t%8f\n\tthroat radius:\t%8f\n\texit radius:\t%8f\n',radius(1),min(radius),radius(end));
            fprintf('\tlength:\t%16f\n\tgeometry nodes:\t%8i\n',xcoord(end),geom_size);
        end
    fclose('all'); %close input file
    if debug;fprintf('input file closed.\n');end
    % MANUAL ENTRY
    mw_units = '[kg/mol]';
    temperature_units = '[K]';
    pressure_units = '[Pa]';
    length_units = '[m]';
    angle_units = '[deg]';
%   ===------------===   

%           NOZZLE NOMENCLATURE
%   ********************************
%
%              /-
%             /         0 = total parameters
%     ===\---/          1 = chamber
%     (1) (2)  (3)      2 = throat
%     ===/---\          3 = exit
%             \
%              \-
%   ********************************

% % ASSUMPTIONS
% - Isentropic flow
% - Initial temperature and pressure are total parameters

    R = R_0/mw; % gas constant
    R_units = '[J/kg K]';
%     A_e = pi*exit_radius^2; % exit area
%     A_t = pi*throat_radius^2; % throat area
    A=pi.*radius.^2;
    area_units = '[m^2]';
    
    A_t=min(A);
    T_star=T_0*(2/(k+1)); %K
    P_star=(2/(k+1))^(k/(k-1)); %Pa
    rho_star=P_star/(R*T_star); % kg/m^3
    mdot=rho_star*sqrt(k*R*T_star)*A_t; %choked
    
    M_idx=linspace(.1,4,length(xcoord));
    k1=(2/(k+1));
    k2=((k-1)/2);
    k3=(.5*(k+1)/(k-1));
    area_ratio=(1./M_idx).*((2/(k+1))*(1+((k-1)/2)*M_idx.^2)).^(.5*(k+1)/(k-1));

    M=zeros(length(xcoord),1);M_sub=M;M_sup=M;temp_ratio=M;T=M;pres_ratio=M;P=M;
    M(1)=0;
    choked=false;
    for x=2:length(xcoord)
            if A(x)<A(x-1)
                M_sub(x)=arearatio2mach_sub(A(x),A_t,k);
            elseif A(x)==A_t 
                if M(x)>=1
                    choked=true
                else
                    disp('flag')
                end          
            else
                M_sup(x)=arearatio2mach_sup(A(x),A_t,k);
                M_sub(x)=arearatio2mach_sub(A(x),A_t,k);
            end
            temp_ratio(x)=(1+((k-1)/2)*M(x)^2);
            T(x)=T_0/temp_ratio(x);
            pres_ratio(x)=temp_ratio(x)^(k/(k-1));
            P(x)=P_0/pres_ratio(x);     
            
            temp_ratio_sub(x)=(1+((k-1)/2)*M_sub(x)^2);
            T_sub(x)=T_0/temp_ratio_sub(x);
            pres_ratio_sub(x)=temp_ratio_sub(x)^(k/(k-1));
            P_sub(x)=P_0/pres_ratio_sub(x); 
            temp_ratio_sup(x)=(1+((k-1)/2)*M_sup(x)^2);
            T_sup(x)=T_0/temp_ratio_sup(x);
            pres_ratio_sup(x)=temp_ratio_sup(x)^(k/(k-1));
            P_sup(x)=P_0/pres_ratio_sup(x); 
    end
    if debug
        figure
        numplots=4;plotcounter=1;
        subplot(numplots,1,plotcounter)
        plot(xcoord,radius);ylabel('radius');plotcounter=plotcounter+1;axis([0 xcoord(end) 0 inf]);
%         subplot(numplots,1,plotcounter)
%         semilogy(xcoord,A./A_t,xcoord(mark),A(mark)./A_t,'x');ylabel('A/A_t');plotcounter=plotcounter+1;
        subplot(numplots,1,plotcounter)
        plot(xcoord,M_sub,xcoord,M_sup);ylabel('M');plotcounter=plotcounter+1;axis([0 xcoord(end) 0 inf]);
        subplot(numplots,1,plotcounter)
        plot(xcoord,T_sub,xcoord,T_sup);ylabel('T');plotcounter=plotcounter+1;axis([0 xcoord(end) 0 inf]);
        subplot(numplots,1,plotcounter)
        plot(xcoord,P_sub/10^3,xcoord,P_sup/10^3);ylabel('P');plotcounter=plotcounter+1;axis([0 xcoord(end) 0 inf]);
%         figure
%         semilogy(M(1:find(A==A_t)),A(1:find(A==A_t))./A_t,M(find(A==A_t)+1:end),A(find(A==A_t)+1:end)./A_t,'--');xlabel('M');ylabel('A/A_t');
%         figure
%         semilogy(M_idx,area_ratio,M,A./A_t,'--')
    end
%     % format & display outputs
    linedivider='------------';
    result =  {'Propellant','',prop_name;
               linedivider,'','';
               'Specific heat ratio', k, unitless;
               'Molar mass', mw, mw_units;
               'Specific gas constant',R,R_units;
               linedivider,'','';
               'Total temperature', T_0, temperature_units;
               'Total pressure', P_0, pressure_units;
               linedivider,'','';
               'Length',xcoord(end),length_units;
               'Inlet radius',radius(1),length_units;
               'Throat radius', min(radius), length_units;
               'Exit radius', radius(end), length_units;
               'Inlet area',A(1),area_units;
               'Throat area',A_t,area_units;
               'Exit area',A(end),area_units;
%                'Half-angle',alpha, angle_units;
               linedivider,'','';
               'Throat temperature',T(find(A==A_t)),temperature_units;
               'Throat pressure',P(find(A==A_t)),pressure_units;
%                'Mass flow rate',mass_flowrate,mass_flowrate_units;
               linedivider,'','';
               'Exit temperature',T(end),temperature_units;
               'Exit pressure',P(end),pressure_units;
               linedivider,'','';
%                'Exhaust velocity',exit_velocity,velocity_units;
%                'Thrust',thrust,force_units;
%                'Specific impulse',specific_impulse,isp_units;
               linedivider,'','';
               'Exit Mach',M(end),unitless;
               'A/At',A(end)/A_t,unitless;
               'T/T0',T(end)/T_0,unitless;
               'P/P0',P(end)/P_0,unitless;
%                'v/at',exit_velocity/throat_velocity,unitless;
               }; 
    display(result);
end

function Mach = arearatio2mach_sub(A,A_t,k)
%   solve Mach number from area ratio by Newton-Raphson Method. (assume
%   subsonic)
%   https://www.grc.nasa.gov/WWW/winddocs/utilities/b4wind_guide/mach.html
    P = 2/(k+1);
    Q = 1-P;
    R = (A/A_t).^2;
    a = P.^(1/Q);
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
    Mach = sqrt(X);
end
function Mach = arearatio2mach_sup(A,A_t,k)
%   solve Mach number from area ratio by Newton-Raphson Method. (assume
%   supersonic)
%   https://www.grc.nasa.gov/WWW/winddocs/utilities/b4wind_guide/mach.html
    P = 2/(k+1);
    Q = 1-P;
    R = (A/A_t).^((2*Q)/P);
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
        fprintf('\n%24s\t%15.8f\t%s',result{i,:});
    end
    fprintf('\n')
end