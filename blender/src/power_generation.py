import math

import bpy

import numpy as np

from astropy.time import Time
from astropy import units as u

from blender import get_cross_section

from pyquaternion import Quaternion

from skyfield.api import load
from skyfield.positionlib import ICRF

from utils import rotation_quaternion_from_vectors

from astro import eclipse_function, GM_EARTH, R_EARTH, R_SUN
import parse

SOLAR_PANEL_EFFICIENCY = 0.285 # 0.2
PERFORMANCE_RATIO = 1 # 0.75


def generate_power(q_eci2body, t_jd, r, v):
    k = GM_EARTH.to_value(u.km**3 / u.s**2)
    R_sec = R_SUN.to_value(u.km)
    R_pri = R_EARTH.to_value(u.km)

    # Load ephemeris from NASA JPL
    ts = load.timescale()
    planets = load('de421.bsp')

    t = ts.tt_jd(t_jd)

    # Get the position of the sun at the current time in the Geocentric frame
    sun_position = planets['sun'].at(t)

    # To convert this position to the ECI frame, we convert it to an ICRF object
    sun_position_eci = ICRF(sun_position.position.au, t=t)

    sun_eci = sun_position_eci.position.km / np.linalg.norm(
        sun_position_eci.position.km
    )

    eclipse = eclipse_function(k, np.hstack((r, v)), sun_eci, R_sec, R_pri)

    if eclipse >= 0:
        return 0
    else:
        sun_body = q_eci2body.rotate(sun_eci)
        q_body2sun = rotation_quaternion_from_vectors(sun_body, [1, 0, 0])
        cross_section = get_cross_section(q_body2sun)
        # sun_constant = get_sun_constant(t_jd)
        # return cross_section * sun_constant * SOLAR_PANEL_EFFICIENCY * PERFORMANCE_RATIO
        return cross_section


def get_sun_constant(julian_date):
    # Constants for maximum and minimum sun radiation
    max_sun_constant = 1413.0
    min_sun_constant = 1322.0

    # Calculate the amplitude and the mean value
    amplitude = (max_sun_constant - min_sun_constant) / 2.0
    mean_value = (max_sun_constant + min_sun_constant) / 2.0

    # Convert the Julian date to a datetime object
    date = Time(julian_date, format='jd').datetime

    # Get the day of the year
    day_of_year = date.timetuple().tm_yday

    # Adjusted cosine variation around the year
    # We shift by 172 days to reach minimum at late June and maximum in mid December
    variation = math.cos(2.0 * math.pi * (day_of_year - 172) / 365.25)

    # Return sun constant for the given Julian date
    return mean_value - amplitude * variation


def main():
    def generate_data(size, step=0.01):
        angle = np.linspace(0, step * size, size)
        q_eci2body = tuple(Quaternion(axis=[1, 0, 0], degrees=a) for a in angle)

        t_jd = tuple(
            np.linspace(
                2458152.5000000 - step * size / 2,
                2458152.5000000 + step * size / 2, size
            )
        )

        r = tuple(
            np.array(
                [
                    i + step * n
                    for i in [-1062.11041563, -5958.95237065, 318.47154649]
                ]
            ) for n in range(size)
        )
        v = tuple(
            np.array(
                [i + step * n for i in [-7.36150147, 1.48246792, 0.06629659]]
            ) for n in range(size)
        )

        return q_eci2body, t_jd, r, v

    # Generating data
    SIZE = 100
    STEP = 100
    # seq_q_eci2body, seq_t_jd, seq_r, seq_v = generate_data(SIZE, STEP)
    seq_t_jd, seq_q_eci2body, areas, powers, seq_r, seq_v = parse.parse_data()

    # Specify the path to your .blend file
    filepath = "../model/model.blend"

    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=filepath)

    seq_power = list()
    index = 0
    for q_eci2body, t_jd, r, v in zip(seq_q_eci2body, seq_t_jd, seq_r, seq_v):
        index = index + 1
        seq_power.append(generate_power(q_eci2body, t_jd, r, v))
    
    with open('our_area', 'w') as file:
        file.write(str(seq_power))


if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import ast
def rr():
    with open('our_area', 'r') as file:
        seq_power_str = file.read()
    
    return seq_power_str

seq_power = ast.literal_eval(rr())

import parse
_, _, p, _, _, _ = parse.parse_data()

plt.plot(p, label='p')
plt.plot(seq_power, label='seq_power')
plt.title('Two lists on the same plot')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()
plt.show()