function Y = ECI2ECEF(MJD_UTC, Y0, eopdata, astro_constants) %#codegen

[x_pole, y_pole, UT1_UTC, LOD, TAI_UTC] = IERS(eopdata, MJD_UTC, astro_constants);
TT_UTC  = 32.184+TAI_UTC;
MJD_UT1 = MJD_UTC + UT1_UTC / 86400;
MJD_TT = MJD_UTC + TT_UTC / 86400;

% Interval between fundamental date J2000.0 and given date (JC).
t = ((astro_constants.DJM0 - astro_constants.DJ00) + MJD_TT) / astro_constants.DJC;

% Form bias-precession-nutation matrix
NPB = iauPnm06a(t, astro_constants);
% Form Earth rotation matrix
Theta = iauRz(iauGst06(astro_constants.DJM0, MJD_UT1, astro_constants.DJM0, MJD_TT, NPB, astro_constants), eye(3));
% Polar motion matrix (TIRS->ITRS, IERS 2003)
Pi = iauPom00(x_pole, y_pole, iauSp00(t, astro_constants));

% ICRS to ITRS transformation matrix and derivative
S = zeros(3);
S(1, 2) = 1;
S(2, 1) = -1; % Derivative of Earth rotation
% Omega  = 7292115.8553e-11+4.3e-15*( (MJD_UTC-astro_constants.MJD_J2000)/36525 ); % [rad/s]
Omega = astro_constants.omega_Earth - 0.843994809 * 1e-9 * LOD; % IERS
dTheta = Omega * S * Theta; % matrix [1/s]
U = Pi * Theta * NPB; % ICRS to ITRS transformation
dU = Pi * dTheta * NPB; % Derivative [1/s]

% Transformation from ICRS to WGS
r = U * Y0(1:3)';
v = U * Y0(4:6)' + dU * Y0(1:3)';
Y = [r; v];
