clc
clear all
format long g

SAT_Const
constants

% read Earth orientation parameters
fid = fopen('eop19620101.txt','r');
%  ----------------------------------------------------------------------------------------------------
% |  Date    MJD      x         y       UT1-UTC      LOD       dPsi    dEpsilon     dX        dY    DAT
% |(0h UTC)           "         "          s          s          "        "          "         "     s 
%  ----------------------------------------------------------------------------------------------------
eopdata = fscanf(fid,'%i %d %d %i %f %f %f %f %f %f %f %f %i',[13 inf]);
fclose(fid);

year = 2004;
month = 4;
day = 6;
hour = 7;
minute = 51;
second = 28.386009;
MJD_UTC = Mjday(year, month, day, hour, minute, second);

% Interpolated values of Earth orientation parameters yield superior results
rv_ecef = [-1033.4793830, +7901.2952754, +6380.3565958, -3.225636520, -2.872451450, +5.531924446]; % [km]
rv_eci = ECEF2ECI(MJD_UTC, rv_ecef, eopdata, astro_constants)
rv_ecef = ECI2ECEF(MJD_UTC, rv_eci', eopdata, astro_constants)