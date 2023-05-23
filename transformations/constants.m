% Pi
astro_constants.DPI = 3.141592653589793238462643;

% 2Pi
astro_constants.D2PI = 6.283185307179586476925287;

% Radians to degrees
astro_constants.DR2D = 57.29577951308232087679815;

% Degrees to radians
astro_constants.DD2R = 1.745329251994329576923691e-2;

% Radians to arcseconds
astro_constants.DR2AS = 206264.8062470963551564734;

% Arcseconds to radians
astro_constants.DAS2R = 4.848136811095359935899141e-6;

% Seconds of time to radians
astro_constants.DS2R =7.272205216643039903848712e-5;

% Arcseconds in a full circle
astro_constants.TURNAS = 1296000.0;

% Milliarcseconds to radians
astro_constants.DMAS2R = astro_constants.DAS2R / 1e3;

% Length of tropical year B1900 (days)
astro_constants.DTY = 365.242198781;

% Seconds per day.
astro_constants.DAYSEC = 86400.0;

% Days per Julian year
astro_constants.DJY = 365.25;

% Days per Julian century
astro_constants.DJC = 36525.0;

% Days per Julian millennium
astro_constants.DJM = 365250.0;

% Reference epoch (J2000.0), Julian Date
astro_constants.DJ00 = 2451545.0;

% Julian Date of Modified Julian Date zero
astro_constants.DJM0 = 2400000.5;

% Reference epoch (J2000.0), Modified Julian Date
astro_constants.DJM00 = 51544.5;

% 1977 Jan 1.0 as MJD
astro_constants.DJM77 = 43144.0;

% TT minus TAI (s)
astro_constants.TTMTAI = 32.184;

% Astronomical unit (m, IAU 2012)
astro_constants.DAU = 149597870.7e3;

% Speed of light (m/s)
astro_constants.CMPS = 299792458.0;

% Light time for 1 au (s)
astro_constants.AULT = astro_constants.DAU/astro_constants.CMPS;

% Speed of light (au per day)
astro_constants.DC = astro_constants.DAYSEC/astro_constants.AULT;

% L_G = 1 - d(TT)/d(TCG)
astro_constants.ELG = 6.969290134e-10;

% L_B = 1 - d(TDB)/d(TCB), and TDB (s) at TAI 1977/1/1.0
astro_constants.ELB = 1.550519768e-8;
astro_constants.TDB0 = -6.55e-5;

% Schwarzschild radius of the Sun (au)
% = 2 * 1.32712440041e20 / (2.99792458e8)^2 / 1.49597870700e11
astro_constants.SRS = 1.97412574336e-8;

