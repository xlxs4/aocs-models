%  - - - - - - -
%   i a u S 0 6
%  - - - - - - -
%
%  The CIO locator s, positioning the Celestial Intermediate Origin on
%  the equator of the Celestial Intermediate Pole, given the CIP's X,Y
%  coordinates.  Compatible with IAU 2006/2000A precession-nutation.
%
%  This function is part of the International Astronomical Union's
%  SOFA (Standards Of Fundamental Astronomy) software collection.
%
%  Status:  canonical model.
%
%  Given:
%     date1,date2   double    TT as a 2-part Julian Date (Note 1)
%     x,y           double    CIP coordinates (Note 3)
%
%  Returned (function value):
%                   double    the CIO locator s in radians (Note 2)
%
%  Notes:
%
%  1) The TT date date1+date2 is a Julian Date, apportioned in any
%     convenient way between the two arguments.  For example,
%     JD(TT)=2450123.7 could be expressed in any of these ways,
%     among others:
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
%  2) The CIO locator s is the difference between the right ascensions
%     of the same point in two systems:  the two systems are the GCRS
%     and the CIP,CIO, and the point is the ascending node of the
%     CIP equator.  The quantity s remains below 0.1 arcsecond
%     throughout 1900-2100.
%
%  3) The series used to compute s is in fact for s+XY/2, where X and Y
%     are the x and y components of the CIP unit vector;  this series
%     is more compact than a direct series for s would be.  This
%     function requires X,Y to be supplied by the caller, who is
%     responsible for providing values that are consistent with the
%     supplied date.
%
%  4) The model is consistent with the "P03" precession (Capitaine et
%     al. 2003), adopted by IAU 2006 Resolution 1, 2006, and the
%     IAU 2000A nutation (with P03 adjustments).
%
%  Called:
%     iauFal03     mean anomaly of the Moon
%     iauFalp03    mean anomaly of the Sun
%     iauFaf03     mean argument of the latitude of the Moon
%     iauFad03     mean elongation of the Moon from the Sun
%     iauFaom03    mean longitude of the Moon's ascending node
%     iauFave03    mean longitude of Venus
%     iauFae03     mean longitude of Earth
%     iauFapa03    general accumulated precession in longitude
%
%  References:
%
%     Capitaine, N., Wallace, P.T. & Chapront, J., 2003, Astron.
%     Astrophys. 432, 355
%
%     McCarthy, D.D., Petit, G. (eds.) 2004, IERS Conventions (2003),
%     IERS Technical Note No. 32, BKG
%
%  This revision:  2021 May 11
%
%  SOFA release 2021-05-12
%
%  Copyright (C) 2021 IAU SOFA Board.  See notes at end.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function s = iauS06(date1, date2, x, y, astro_constants)

% t: Time since J2000.0, in Julian centuries
% fa[8]: Fundamental arguments
% nfa[8]: coefficients of l,l',F,D,Om,LVe,LE,pA
% s, c:   sine and cosine coefficients

% Polynomial coefficients: 1-6
sp = [94.00e-6, 3808.65e-6, -122.68e-6, -72574.11e-6, 27.98e-6, 15.62e-6];

% Terms of order t^0
s0 = [
% 1-10
 0,  0,  0,  0,  1,  0,  0,  0, -2640.73e-6,   0.39e-6;
 0,  0,  0,  0,  2,  0,  0,  0,   -63.53e-6,   0.02e-6;
 0,  0,  2, -2,  3,  0,  0,  0,   -11.75e-6,  -0.01e-6;
 0,  0,  2, -2,  1,  0,  0,  0,   -11.21e-6,  -0.01e-6;
 0,  0,  2, -2,  2,  0,  0,  0,     4.57e-6,   0.00e-6;
 0,  0,  2,  0,  3,  0,  0,  0,    -2.02e-6,   0.00e-6;
 0,  0,  2,  0,  1,  0,  0,  0,    -1.98e-6,   0.00e-6;
 0,  0,  0,  0,  3,  0,  0,  0,     1.72e-6,   0.00e-6;
 0,  1,  0,  0,  1,  0,  0,  0,     1.41e-6,   0.01e-6;
 0,  1,  0,  0, -1,  0,  0,  0,     1.26e-6,   0.01e-6;
% 11-20
 1,  0,  0,  0, -1,  0,  0,  0,     0.63e-6,   0.00e-6;
 1,  0,  0,  0,  1,  0,  0,  0,     0.63e-6,   0.00e-6;
 0,  1,  2, -2,  3,  0,  0,  0,    -0.46e-6,   0.00e-6;
 0,  1,  2, -2,  1,  0,  0,  0,    -0.45e-6,   0.00e-6;
 0,  0,  4, -4,  4,  0,  0,  0,    -0.36e-6,   0.00e-6;
 0,  0,  1, -1,  1, -8, 12,  0,     0.24e-6,   0.12e-6;
 0,  0,  2,  0,  0,  0,  0,  0,    -0.32e-6,   0.00e-6;
 0,  0,  2,  0,  2,  0,  0,  0,    -0.28e-6,   0.00e-6;
 1,  0,  2,  0,  3,  0,  0,  0,    -0.27e-6,   0.00e-6;
 1,  0,  2,  0,  1,  0,  0,  0,    -0.26e-6,   0.00e-6;
% 21-30
 0,  0,  2, -2,  0,  0,  0,  0,     0.21e-6,   0.00e-6;
 0,  1, -2,  2, -3,  0,  0,  0,    -0.19e-6,   0.00e-6;
 0,  1, -2,  2, -1,  0,  0,  0,    -0.18e-6,   0.00e-6;
 0,  0,  0,  0,  0,  8,-13, -1,     0.10e-6,  -0.05e-6;
 0,  0,  0,  2,  0,  0,  0,  0,    -0.15e-6,   0.00e-6;
 2,  0, -2,  0, -1,  0,  0,  0,     0.14e-6,   0.00e-6;
 0,  1,  2, -2,  2,  0,  0,  0,     0.14e-6,   0.00e-6;
 1,  0,  0, -2,  1,  0,  0,  0,    -0.14e-6,   0.00e-6;
 1,  0,  0, -2, -1,  0,  0,  0,    -0.14e-6,   0.00e-6;
 0,  0,  4, -2,  4,  0,  0,  0,    -0.13e-6,   0.00e-6;
% 31-33
 0,  0,  2, -2,  4,  0,  0,  0,     0.11e-6,   0.00e-6;
 1,  0, -2,  0, -3,  0,  0,  0,    -0.11e-6,   0.00e-6;
 1,  0, -2,  0, -1,  0,  0,  0,    -0.11e-6,   0.00e-6];

% Terms of order t^1
s1 = [
% 1 - 3
 0,  0,  0,  0,  2,  0,  0,  0,    -0.07e-6,   3.57e-6;
 0,  0,  0,  0,  1,  0,  0,  0,     1.73e-6,  -0.03e-6;
 0,  0,  2, -2,  3,  0,  0,  0,     0.00e-6,   0.48e-6];

% Terms of order t^2
s2 = [
% 1-10
 0,  0,  0,  0,  1,  0,  0,  0,   743.52e-6,  -0.17e-6;
 0,  0,  2, -2,  2,  0,  0,  0,    56.91e-6,   0.06e-6;
 0,  0,  2,  0,  2,  0,  0,  0,     9.84e-6,  -0.01e-6;
 0,  0,  0,  0,  2,  0,  0,  0,    -8.85e-6,   0.01e-6;
 0,  1,  0,  0,  0,  0,  0,  0,    -6.38e-6,  -0.05e-6;
 1,  0,  0,  0,  0,  0,  0,  0,    -3.07e-6,   0.00e-6;
 0,  1,  2, -2,  2,  0,  0,  0,     2.23e-6,   0.00e-6;
 0,  0,  2,  0,  1,  0,  0,  0,     1.67e-6,   0.00e-6;
 1,  0,  2,  0,  2,  0,  0,  0,     1.30e-6,   0.00e-6;
 0,  1, -2,  2, -2,  0,  0,  0,     0.93e-6,   0.00e-6;
% 11-20
 1,  0,  0, -2,  0,  0,  0,  0,     0.68e-6,   0.00e-6;
 0,  0,  2, -2,  1,  0,  0,  0,    -0.55e-6,   0.00e-6;
 1,  0, -2,  0, -2,  0,  0,  0,     0.53e-6,   0.00e-6;
 0,  0,  0,  2,  0,  0,  0,  0,    -0.27e-6,   0.00e-6;
 1,  0,  0,  0,  1,  0,  0,  0,    -0.27e-6,   0.00e-6;
 1,  0, -2, -2, -2,  0,  0,  0,    -0.26e-6,   0.00e-6;
 1,  0,  0,  0, -1,  0,  0,  0,    -0.25e-6,   0.00e-6;
 1,  0,  2,  0,  1,  0,  0,  0,     0.22e-6,   0.00e-6;
 2,  0,  0, -2,  0,  0,  0,  0,    -0.21e-6,   0.00e-6;
 2,  0, -2,  0, -1,  0,  0,  0,     0.20e-6,   0.00e-6;
% 21-25
 0,  0,  2,  2,  2,  0,  0,  0,     0.17e-6,   0.00e-6;
 2,  0,  2,  0,  2,  0,  0,  0,     0.13e-6,   0.00e-6;
 2,  0,  0,  0,  0,  0,  0,  0,    -0.13e-6,   0.00e-6;
 1,  0,  2, -2,  2,  0,  0,  0,    -0.12e-6,   0.00e-6;
 0,  0,  2,  0,  0,  0,  0,  0,    -0.11e-6,   0.00e-6];

% Terms of order t^3
s3 = [
% 1-4
 0,  0,  0,  0,  1,  0,  0,  0,     0.30e-6, -23.42e-6;
 0,  0,  2, -2,  2,  0,  0,  0,    -0.03e-6,  -1.46e-6;
 0,  0,  2,  0,  2,  0,  0,  0,    -0.01e-6,  -0.25e-6;
 0,  0,  0,  0,  2,  0,  0,  0,     0.00e-6,   0.23e-6];

% Terms of order t^4
s4 = [
% 1-1
 0,  0,  0,  0,  1,  0,  0,  0,    -0.26e-6,  -0.01e-6];

% Number of terms in the series
[NS0, ~] = size(s0);
[NS1, ~] = size(s1);
[NS2, ~] = size(s2);
[NS3, ~] = size(s3);
[NS4, ~] = size(s4);

% ------------------------------------------------------------------

% Interval between fundamental epoch J2000.0 and current date (JC).
t = ((date1 - astro_constants.DJ00) + date2) / astro_constants.DJC;

% Fundamental Arguments (from IERS Conventions 2003)

% Mean anomaly of the Moon.
fa(1) = rem(            485868.249036 +...
    t * ( 1717915923.2178 +...
    t * (         31.8792 +...
    t * (          0.051635 +...
    t * (        - 0.00024470 ) ) ) ), astro_constants.TURNAS ) * astro_constants.DAS2R;

% Mean anomaly of the Sun.
fa(2) = rem(          1287104.793048 +...
    t * ( 129596581.0481 +...
    t * (       - 0.5532 +...
    t * (         0.000136 +...
    t * (       - 0.00001149 ) ) ) ), astro_constants.TURNAS ) * astro_constants.DAS2R;

% Mean longitude of the Moon minus that of the ascending node.
fa(3) = rem(            335779.526232 +...
    t * ( 1739527262.8478 +...
    t * (       - 12.7512 +...
    t * (        - 0.001037 +...
    t * (          0.00000417 ) ) ) ), astro_constants.TURNAS ) * astro_constants.DAS2R;

% Mean elongation of the Moon from the Sun.
fa(4) = rem(           1072260.703692 +...
    t * ( 1602961601.2090 +...
    t * (        - 6.3706 +...
    t * (          0.006593 +...
    t * (        - 0.00003169 ) ) ) ), astro_constants.TURNAS ) * astro_constants.DAS2R;

% Mean longitude of the ascending node of the Moon.
fa(5) = rem(           450160.398036 +...
    t * ( - 6962890.5431 +...
    t * (         7.4722 +...
    t * (         0.007702 +...
    t * (       - 0.00005939 ) ) ) ), astro_constants.TURNAS ) * astro_constants.DAS2R;

% Mean longitude of Venus.
fa(6) = rem(3.176146697 + 1021.3285546211 * t, astro_constants.D2PI);

% Mean longitude of Earth.
fa(7) = rem(1.753470314 + 628.3075849991 * t, astro_constants.D2PI);

% General precession in longitude.
fa(8) = (0.024381750 + 0.00000538691 * t) * t;

% Evaluate s.
w0 = sp(1);
w1 = sp(2);
w2 = sp(3);
w3 = sp(4);
w4 = sp(5);
w5 = sp(6);

for i =NS0:-1:1
    a = 0;
    for j = 1:8
        a = a + s0(i,j) * fa(j);
    end
    w0 = w0 + s0(i,9) * sin(a) + s0(i,10) * cos(a);
end

for i =NS1:-1:1
    a = 0;
    for j = 1:8
        a = a + s1(i,j) * fa(j);
    end
    w1 = w1 + s1(i,9) * sin(a) + s1(i,10) * cos(a);
end

for i =NS2:-1:1
    a = 0;
    for j = 1:8
        a = a + s2(i,j) * fa(j);
    end
    w2 = w2 + s2(i,9) * sin(a) + s2(i,10) * cos(a);
end

for i =NS3:-1:1
    a = 0;
    for j = 1:8
        a = a + s3(i,j) * fa(j);
    end
    w3 = w3 + s3(i,9) * sin(a) + s3(i,10) * cos(a);
end

for i =NS4:-1:1
    a = 0;
    for j = 1:8
        a = a + s4(i,j) * fa(j);
    end
    w4 = w4 + s4(i,9) * sin(a) + s4(i,10) * cos(a);
end

s = (w0 + (w1 + (w2 + (w3 + (w4 + w5 * t) * t) * t) * t) * t) * astro_constants.DAS2R - x*y/2.0;

