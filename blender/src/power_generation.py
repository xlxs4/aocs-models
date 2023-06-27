import numpy as np

from astropy import units as u

from blender import get_cross_section

from pyquaternion import Quaternion

from skyfield.api import load
from skyfield.positionlib import ICRF

from utils import rotation_quaternion_from_vectors

from astro import eclipse_function, GM_EARTH, R_EARTH, R_SUN

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

r, v = (
    np.array([-1062.11041563, -5958.95237065,
              318.47154649]), np.array([-7.36150147, 1.48246792, 0.06629659])
)

eclipse = eclipse_function(k, np.hstack((r, v)), sun_eci, R_sec, R_pri)
print(eclipse)
