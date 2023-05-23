function [x_pole,y_pole,UT1_UTC,LOD,TAI_UTC] = IERS(eop,Mjd_UTC,astro_constants)

% linear interpolation
mjd = floor(Mjd_UTC);
i = find(mjd==eop(4,:),1,'first');
preeop = eop(:,i);
nexteop = eop(:,i+1);
fixf = Mjd_UTC-mjd;
% Setting of IERS Earth rotation parameters
% (UT1-UTC [s], TAI-UTC [s], x ["], y ["])
x_pole  = preeop(5)+(nexteop(5)-preeop(5))*fixf;
y_pole  = preeop(6)+(nexteop(6)-preeop(6))*fixf;
UT1_UTC = preeop(7)+(nexteop(7)-preeop(7))*fixf;
LOD     = preeop(8)+(nexteop(8)-preeop(8))*fixf;
TAI_UTC = preeop(13);

x_pole  = x_pole/astro_constants.Arcs;  % Pole coordinate [rad]
y_pole  = y_pole/astro_constants.Arcs;  % Pole coordinate [rad]
