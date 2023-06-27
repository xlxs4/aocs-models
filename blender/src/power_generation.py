from utils import rotation_quaternion_from_vectors
import numpy as np
from pyquaternion import Quaternion
from skyfield.api import Topos, load
from skyfield.positionlib import ICRF
from blender import get_cross_section
from numpy.linalg import norm
from numpy import cross, sqrt, cos, sin

from astropy.constants import Constant
from astropy import units as u


def eclipse_function(k, u_, r_sec, R_sec, R_primary, umbra=True):
    """Calculates a continuous shadow function.

    Parameters
    ----------
    k : float
        Standard gravitational parameter (km^3 / s^2).
    u_ : numpy.ndarray
        Satellite position and velocity vector with respect to the primary body.
    r_sec : numpy.ndarray
        Position vector of the secondary body with respect to the primary body.
    R_sec : float
        Equatorial radius of the secondary body.
    R_primary : float
        Equatorial radius of the primary body.
    umbra : bool
        Whether to calculate the shadow function for umbra or penumbra, defaults to True
        i.e. calculates for umbra.

    Notes
    -----
    The shadow function is taken from Escobal, P. (1985). Methods of orbit determination.
    The current implementation assumes circular bodies and doesn't account for flattening.

    """
    # Plus or minus condition
    pm = 1 if umbra else -1
    p, ecc, inc, raan, argp, nu = rv2coe(k, u_[:3], u_[3:])

    PQW = coe_rotation_matrix(inc, raan, argp)
    # Make arrays contiguous for faster dot product with numba.
    P_, Q_ = np.ascontiguousarray(PQW[:, 0]), np.ascontiguousarray(PQW[:, 1])

    r_sec_norm = norm(r_sec)
    beta = (P_ @ r_sec) / r_sec_norm
    zeta = (Q_ @ r_sec) / r_sec_norm

    sin_delta_shadow = np.sin((R_sec - pm * R_primary) / r_sec_norm)

    cos_psi = beta * np.cos(nu) + zeta * np.sin(nu)
    shadow_function = (
        ((R_primary**2) * (1 + ecc * np.cos(nu))**2) + (p**2) * (cos_psi**2) -
        p**2 + pm * (2 * p * R_primary * cos_psi) *
        (1 + ecc * np.cos(nu)) * sin_delta_shadow
    )

    return shadow_function


def rv2coe(k, r, v, tol=1e-8):
    r"""Converts from vectors to classical orbital elements.

    Parameters
    ----------
    k : float
        Standard gravitational parameter (km^3 / s^2)
    r : numpy.ndarray
        Position vector (km)
    v : numpy.ndarray
        Velocity vector (km / s)
    tol : float, optional
        Tolerance for eccentricity and inclination checks, default to 1e-8

    Returns
    -------
    p : float
        Semi-latus rectum of parameter (km)
    ecc: float
        Eccentricity
    inc: float
        Inclination (rad)
    raan: float
        Right ascension of the ascending nod (rad)
    argp: float
        Argument of Perigee (rad)
    nu: float
        True Anomaly (rad)



    """
    h = cross(r, v)
    n = cross([0, 0, 1], h)
    e = ((v @ v - k / norm(r)) * r - (r @ v) * v) / k
    ecc = norm(e)
    p = (h @ h) / k
    inc = np.arccos(h[2] / norm(h))

    circular = ecc < tol
    equatorial = abs(inc) < tol

    if equatorial and not circular:
        raan = 0
        argp = np.arctan2(e[1], e[0]) % (2 * np.pi)  # Longitude of periapsis
        nu = np.arctan2((h @ cross(e, r)) / norm(h), r @ e)
    elif not equatorial and circular:
        raan = np.arctan2(n[1], n[0]) % (2 * np.pi)
        argp = 0
        # Argument of latitude
        nu = np.arctan2((r @ cross(h, n)) / norm(h), r @ n)
    elif equatorial and circular:
        raan = 0
        argp = 0
        nu = np.arctan2(r[1], r[0]) % (2 * np.pi)  # True longitude
    else:
        a = p / (1 - (ecc**2))
        ka = k * a
        if a > 0:
            e_se = (r @ v) / sqrt(ka)
            e_ce = norm(r) * (v @ v) / k - 1
            nu = E_to_nu(np.arctan2(e_se, e_ce), ecc)
        else:
            e_sh = (r @ v) / sqrt(-ka)
            e_ch = norm(r) * (norm(v)**2) / k - 1
            nu = F_to_nu(np.log((e_ch + e_sh) / (e_ch - e_sh)) / 2, ecc)

        raan = np.arctan2(n[1], n[0]) % (2 * np.pi)
        px = r @ n
        py = (r @ cross(h, n)) / norm(h)
        argp = (np.arctan2(py, px) - nu) % (2 * np.pi)

    nu = (nu + np.pi) % (2 * np.pi) - np.pi

    return p, ecc, inc, raan, argp, nu


def E_to_nu(E, ecc):
    r"""True anomaly from eccentric anomaly.

    .. versionadded:: 0.4.0

    Parameters
    ----------
    E : float
        Eccentric anomaly in radians.
    ecc : float
        Eccentricity.

    Returns
    -------
    nu : float
        True anomaly, between -π and π radians.

    """
    nu = 2 * np.arctan(np.sqrt((1 + ecc) / (1 - ecc)) * np.tan(E / 2))
    return nu


def F_to_nu(F, ecc):
    r"""True anomaly from hyperbolic anomaly.

    Parameters
    ----------
    F : float
        Hyperbolic anomaly.
    ecc : float
        Eccentricity (>1).

    Returns
    -------
    nu : float
        True anomaly.

    """
    nu = 2 * np.arctan(np.sqrt((ecc + 1) / (ecc - 1)) * np.tanh(F / 2))
    return nu


def coe_rotation_matrix(inc, raan, argp):
    """Create a rotation matrix for coe transformation."""
    r = rotation_matrix(raan, 2)
    r = r @ rotation_matrix(inc, 0)
    r = r @ rotation_matrix(argp, 2)
    return r


def rotation_matrix(angle, axis):
    assert axis in (0, 1, 2)
    angle = np.asarray(angle)
    c = cos(angle)
    s = sin(angle)

    a1 = (axis + 1) % 3
    a2 = (axis + 2) % 3
    R = np.zeros(angle.shape + (3, 3))
    R[..., axis, axis] = 1.0
    R[..., a1, a1] = c
    R[..., a1, a2] = -s
    R[..., a2, a1] = s
    R[..., a2, a2] = c
    return R


GM_EARTH = Constant(
    "GM_earth",
    "Geocentric gravitational constant",
    3.986004418e14,
    "m3 / (s2)",
    0.000000008e14,
    "IAU 2009 system of astronomical constants",
    system="si",
)

R_EARTH = Constant(
    "R_earth",
    "Earth equatorial radius",
    6.3781366e6,
    "m",
    0.1,
    "IAU Working Group on Cartographic Coordinates and Rotational Elements: 2015",
    system="si",
)

R_SUN = Constant(
    "R_sun",
    "Sun equatorial radius",
    6.95700e8,
    "m",
    0,
    "IAU Working Group on Cartographic Coordinates and Rotational Elements: 2015",
    system="si",
)

k = GM_EARTH.to_value(u.km**3 / u.s**2)
R_sec = R_SUN.to_value(u.km)
R_pri = R_EARTH.to_value(u.km)

# Load ephemeris from NASA JPL
ts = load.timescale()
planets = load('de421.bsp')

# Get current time
t = ts.now()

# Get the position of the sun at the current time in the Geocentric frame
sun_position = planets['sun'].at(t)

# To convert this position to the ECI frame, we convert it to an ICRF object
sun_position_eci = ICRF(sun_position.position.au, t=t)

# Display position
sun_eci = sun_position_eci.position.km / np.linalg.norm(
    sun_position_eci.position.km
)

# position_eci = [1,1,1]
q_eci2body = [Quaternion([1, 0, 0, 0])]
sun_body = q_eci2body[0].rotate(sun_eci)
q_body2sun = rotation_quaternion_from_vectors(sun_body, [1, 0, 0])

cross_section = get_cross_section(q_body2sun)

r, v = (np.array([1, 1, 1]), np.array([0.5, 1, -0.5]))

eclipse = eclipse_function(k, np.hstack((r, v)), sun_eci, R_sec, R_pri)
print(eclipse)
#  Position vector of Sun wrt Solar System Barycenter
# r_sec_ssb = get_body_barycentric_posvel("Sun", orbit.epoch)[0]
# r_pri_ssb = get_body_barycentric_posvel("Earth", orbit.epoch)[0]

# r_sec = ((r_sec_ssb - r_pri_ssb).xyz << u.km).value

# rr = (rr << u.km).value
# vv = (vv << u.km / u.s).value

# eclipses = []  # List to store values of eclipse_function.
# for i in range(len(rr)):
#     r = rr[i]
#     v = vv[i]
#     eclipse = eclipse_function(k, np.hstack((r, v)), r_sec, R_sec, R_pri)
#     eclipses.append(eclipse)

# plt.xlabel("Time (s)")
# plt.ylabel("Eclipse function")
# plt.title("Eclipse function vs time")
# plt.plot(tofs[: len(rr)].to_value(u.s), eclipses)
