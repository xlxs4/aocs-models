import itertools
import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as R
from skyfield.api import load

from config import config
from eltypes import ICRF, Quaternion, SpiceKernel, Time


def align_with_sun_and_nadir(
    sun_vector: np.ndarray, nadir_vector: np.ndarray
) -> Quaternion:
    sun_vector_norm, nadir_vector_norm = np.linalg.norm(
        sun_vector
    ), np.linalg.norm(nadir_vector)
    sun_vector, nadir_vector = sun_vector / sun_vector_norm, nadir_vector / nadir_vector_norm

    # Calculate the satellite body frame
    x_sat = -sun_vector
    y_sat = (
        nadir_vector - sun_vector * np.dot(sun_vector, nadir_vector)
    ) / sun_vector_norm  # remove the component of nadir_vector that is in the direction of sun_vector
    z_sat = np.cross(x_sat, y_sat) / np.linalg.norm(
        np.cross(x_sat, y_sat)
    )  # z is now perpendicular to both x and y

    rotation_matrix = np.vstack((x_sat, y_sat, z_sat))
    quat = R.from_matrix(rotation_matrix).as_quat()

    return Quaternion([quat[3], quat[0], quat[1], quat[2]])


def sun_constant(julian_date: np.float64) -> float:
    amplitude = (config.max_sun_constant - config.min_sun_constant) / 2.0
    mean_value = (config.max_sun_constant + config.min_sun_constant) / 2.0

    date = Time(julian_date, format='jd').datetime
    day_of_year = date.timetuple().tm_yday
    variation = math.cos(2.0 * math.pi * (day_of_year - 172) / 365.25)

    return mean_value - amplitude * variation


def time_sequence(t_jd: List[Time]) -> Time:
    return load.timescale().utc(
        t_jd[0].value.year, t_jd[0].value.month, t_jd[0].value.day,
        t_jd[0].value.hour, t_jd[0].value.minute, range(0,
                                                        len(t_jd) * 10, 10)
    )


def sun_position(eph: SpiceKernel, t: List) -> ICRF:
    sun = eph['sun']
    earth = eph['earth']

    astrometric = earth.at(t).observe(sun)
    apparent = astrometric.apparent()

    sun_position = apparent.position.au
    sun_position_eci = ICRF(sun_position, t=t)

    return sun_position_eci


def plot_data(
    x: List,
    y1: List,
    y2: List,
    title: str,
    xlabel: str,
    ylabel: str,
    legend_labels: List[str],
    accumulate: bool = False
):
    if accumulate:
        y1 = list(itertools.accumulate(y1))
        y2 = list(itertools.accumulate(y2))

    plt.scatter(x, y1, s=10, label=legend_labels[0])
    plt.scatter(x, y2, s=10, label=legend_labels[1])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()

import numpy as np

def perifocal_to_cartesian(r_pf, v_pf, i, raan, argp):
    # Convert angles to radians
    i = np.radians(i)
    raan = np.radians(raan)
    argp = np.radians(argp)

    # Rotation matrix
    R = np.array([
        [np.cos(raan) * np.cos(argp) - np.sin(raan) * np.sin(argp) * np.cos(i), 
         -np.cos(raan) * np.sin(argp) - np.sin(raan) * np.cos(argp) * np.cos(i), 
         np.sin(raan) * np.sin(i)],
        [np.sin(raan) * np.cos(argp) + np.cos(raan) * np.sin(argp) * np.cos(i), 
         -np.sin(raan) * np.sin(argp) + np.cos(raan) * np.cos(argp) * np.cos(i), 
         -np.cos(raan) * np.sin(i)],
        [np.sin(argp) * np.sin(i), 
         np.cos(argp) * np.sin(i), 
         np.cos(i)]
    ])

    # Perform the rotation
    r_xyz = np.dot(R, r_pf)
    v_xyz = np.dot(R, v_pf)

    return r_xyz, v_xyz

def calculate_mean_motion(semi_major_axis_km):
    # Gravitational constant of Earth in km^3/s^2
    mu = 398600.4418  

    # Calculate the mean motion (rad/sec)
    n_rad_per_sec = np.sqrt(mu / semi_major_axis_km**3)
    
    # Convert mean motion from rad/sec to rev/day
    n_rev_per_day = n_rad_per_sec * (24*60*60) / (2*np.pi)

    return n_rev_per_day

def orbital_elements_to_tle(a, e, i, raan, argp, nu, epoch):
    # Use astropy to create a state vector from Keplerian elements
    mu = 398600.4418  # gravitational parameter of the Earth in km^3/s^2
    n = calculate_mean_motion(a)
    nu_rad = np.radians(nu)  # convert nu to radians
    r = a * (1 - e**2) / (1 + e * np.cos(nu_rad))  # radius
    v = np.sqrt(mu * (2./r - 1./a))  # velocity magnitude

    # Compute position and velocity vectors in the perifocal frame
    r_pf = np.array([r * np.cos(nu_rad), r * np.sin(nu_rad), 0])
    v_pf = np.array([-v * np.sin(nu_rad), v * (e + np.cos(nu_rad)), 0])

    # Convert to Cartesian coordinates in the ICRS frame
    r_xyz, v_xyz = perifocal_to_cartesian(r_pf, v_pf, i, raan, argp)

    # Now create the fake TLE with these vectors
    line1 = f'1 00005U 58002B   {epoch.to_datetime().strftime("%y%j.%f")[2:]}  .00000023  00000-0  28098-4 0  4753'
    line2 = f'2 00005  {i:.4f} {raan:.4f} {e:.7f} {argp:.4f} {nu:.4f} {n:.4f} 0'

    return line1, line2
