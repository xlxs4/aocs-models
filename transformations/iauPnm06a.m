%  - - - - - - - - - -
%   i a u P n m 0 6 a
%  - - - - - - - - - -
%
%  Form the matrix of precession-nutation for a given date (including
%  frame bias), equinox based, IAU 2006 precession and IAU 2000A
%  nutation models.
%
%  This function is part of the International Astronomical Union's
%  SOFA (Standards Of Fundamental Astronomy) software collection.
%
%  Status:  support function.
%
%  Given:
%     date1,date2 double       TT as a 2-part Julian Date (Note 1)
%
%  Returned:
%     rbpn        double[3][3] bias-precession-nutation matrix (Note 2)
%
%  Notes:
%
%  1) The TT date date1+date2 is a Julian Date, apportioned in any
%     convenient way between the two arguments.  For example,
%     JD(TT)=2450123.7 could be expressed in any of these ways, among
%     others:
%
%            date1          date2
%
%         2450123.7           0.0       (JD method)
%         2451545.0       -1421.3       (J2000 method)
%         2400000.5       50123.2       (MJD method)
%         2450123.5           0.2       (date & time method)
%
%     The JD method is the most natural and convenient to use in
%     cases where the loss of several decimal digits of resolution
%     is acceptable.  The J2000 method is best matched to the way
%     the argument is handled internally and will deliver the
%     optimum resolution.  The MJD method and the date & time methods
%     are both good compromises between resolution and convenience.
%
%  2) The matrix operates in the sense V(date) = rbpn * V(GCRS), where
%     the p-vector V(date) is with respect to the true equatorial triad
%     of date date1+date2 and the p-vector V(GCRS) is with respect to
%     the Geocentric Celestial Reference System (IAU, 2000).
%
%  Called:
%     iauPfw06     bias-precession F-W angles, IAU 2006
%     iauNut06a    nutation, IAU 2006/2000A
%     iauFw2m      F-W angles to r-matrix
%
%  Reference:
%
%     Capitaine, N. & Wallace, P.T., 2006, Astron.Astrophys. 450, 855.
%
%  This revision:  2021 May 11
%
%  SOFA release 2021-05-12
%
%  Copyright (C) 2021 IAU SOFA Board.  See notes at end.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function rbpn = iauPnm06a(t, astro_constants)


% Fukushima-Williams angles for frame bias and precession.
[gamb, phib, psib, epsa] = iauPfw06(t, astro_constants);

% Nutation components.
[dp, de] = iauNut00a(t, astro_constants);

% Factor correcting for secular variation of J2.
fj2 = -2.7774e-6 * t;

% Apply P03 adjustments (Wallace & Capitaine, 2006, Eqs.5).
dpsi = dp + dp * (0.4697e-6 + fj2);
deps = de + de * fj2;

% Equinox based nutation x precession x bias matrix.
rbpn = iauFw2m(gamb, phib, psib + dpsi, epsa + deps);

