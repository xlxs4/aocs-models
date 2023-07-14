import itertools
import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time
from pyquaternion import Quaternion
from scipy.spatial.transform import Rotation as R
from skyfield.api import load
from skyfield.jpllib import SpiceKernel
from skyfield.positionlib import ICRF

from config import config


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


def sun_constant(julian_date: float) -> float:
    amplitude = (config.max_sun_constant - config.min_sun_constant) / 2.0
    mean_value = (config.max_sun_constant + config.min_sun_constant) / 2.0

    date = Time(julian_date, format='jd').datetime
    day_of_year = date.timetuple().tm_yday
    variation = math.cos(2.0 * math.pi * (day_of_year - 172) / 365.25)

    return mean_value - amplitude * variation


def time_sequence(t_jd) -> List:
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
