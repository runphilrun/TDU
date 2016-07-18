# NozzleDesign
Thruster nozzle design tool written in python

## Purpose
Aid design and analysis of engine nozzles for SmallSat and CubeSat monopropellant thrusters in space.

## References 
Sutton, George P., Biblarz, Oscar. Rocket Propulsion Elements (8th Edition). 2010.

This document follows the symbol and formulation conventions used in 
Rocket Propulsion Elements (Sutton).

## Assumptions for ideal rocket
1.    The working substance (or chemical reaction products) is homogeneous.
2.    All the species of the working fluid are gaseous. Any condensed phases (liquid or solid) add a negligible amount to the total mass.
3.    The working substance obeys the perfect gas law.
4.    There is no heat transfer across the rocket walls; therefore, the flow is adiabatic.
5.    There is no appreciable friction and all boundary layer effects are neglected.
6.    There are no shock waves or discontinuities in the nozzle flow.
7.    The propellant flow is steady and constant. The expansion of the working fluid is uniform and steady, without vibration. Transient effects (i.e., start-up and shutdown) are of very short duration and may be neglected.
8.    All exhaust gases leaving the rocket have an axially directed velocity.
9.    The gas velocity, pressure, temperature, and density are all uniform across any section normal to the nozzle axis.
10.   Chemical equilibrium is established within the rocket chamber and the gas composition does not change in the nozzle (frozen flow).
11.   Stored propellants are at room temperature. Cryogenic propellants are at their boiling points.

## Usage
Edit *config.ini* to set values for the propellant gas properties, nozzle mass properties, and chamber thermodynamic properties. By default, the values assume gaseous Nitrogen propellant, Aluminum T6-6061 nozzle .125" thick, chamber pressure at around 300 psi and chamber temperature at 273 K.


