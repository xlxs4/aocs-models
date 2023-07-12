import math
from typing import List
from dataclasses import dataclass
from astropy.time import Time
import bpy
import numpy as np
from skyfield.api import load
from skyfield.positionlib import ICRF
from utils import align_with_sun_and_nadir
from blender import get_cross_section
import parse
import matplotlib.pyplot as plt
import itertools
import pyquaternion


@dataclass
class Config:
    solar_panel_efficiency: float = 0.285
    performance_ratio: float = 1
    max_sun_constant: float = 1413.0
    min_sun_constant: float = 1322.0
    filepath: str = "../model/new_model.blend"
    stations_url: str = 'http://celestrak.org/NORAD/elements/stations.txt'
    output_file: str = 'our_power'


config = Config()


def generate_power(
    q_eci2body: np.ndarray, nadir_body: np.ndarray, sun_position_eci_km: np.ndarray, sun_constant: float
) -> float:
    # q_eci2body = pyquaternion.Quaternion(0.18257418583505536, 0.3651483716701107, 0.5477225575051661, 0.7302967433402214)
    # sun_eci = np.array([-38580178.286403, 134985394.198967, 58508288.441649])
    sun_eci = sun_position_eci_km / np.linalg.norm(sun_position_eci_km)   
    sun_eci = sun_eci / np.linalg.norm(sun_eci)
    sun_body = q_eci2body.conjugate.rotate(sun_eci)
    # sun_body = q_eci2body.rotate(sun_eci)
    # q_body2sun = rotation_quaternion_from_vectors(sun_body, [0, -1, 0])
    nadir_body = nadir_body/np.linalg.norm(nadir_body)
    q_body2sun = align_with_sun_and_nadir(sun_body, nadir_body)
    cross_section = get_cross_section(q_body2sun)
    return cross_section * sun_constant * config.solar_panel_efficiency * config.performance_ratio


def get_sun_constant(julian_date: float) -> float:
    amplitude = (config.max_sun_constant - config.min_sun_constant) / 2.0
    mean_value = (config.max_sun_constant + config.min_sun_constant) / 2.0

    date = Time(julian_date, format='jd').datetime
    day_of_year = date.timetuple().tm_yday
    variation = math.cos(2.0 * math.pi * (day_of_year - 172) / 365.25)

    return mean_value - amplitude * variation


def get_time_sequence(t_jd) -> List:
    return load.timescale().utc(
        t_jd[0].value.year, t_jd[0].value.month, t_jd[0].value.day,
        t_jd[0].value.hour, t_jd[0].value.minute, range(0,
                                                        len(t_jd) * 10, 10)
    )


def get_sun_position(t: List) -> ICRF:
    eph = load('de421.bsp')
    sun = eph['sun']
    earth = eph['earth']

    astrometric = earth.at(t).observe(sun)
    apparent = astrometric.apparent()

    sun_position = apparent.position.au
    seq_sun_position_eci = ICRF(sun_position, t=t)

    return seq_sun_position_eci


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

    plt.plot(x, y1, label=legend_labels[0])
    plt.plot(x, y2, label=legend_labels[1])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()


def main():
    t_jd, seq_q_eci2body, areas, powers, _, _ = parse.parse_data()

    bpy.ops.wm.open_mainfile(filepath=config.filepath)

    t = get_time_sequence(t_jd)

    seq_sun_position_eci = get_sun_position(t)

    satellites = load.tle_file(config.stations_url)
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['ISS (ZARYA)']
    geocentric_position = satellite.at(t)
    # 'up' vector is simply the negation of the position, as the vector from satellite to Earth's center
    seq_nadir_body = -geocentric_position.position.km
    sunlit = satellite.at(t).is_sunlit(load('de421.bsp'))

    seq_sun_constant = [get_sun_constant(time.tt) for time in t]

    index = len(powers)
    powers = powers[:index]
    areas = areas[:index]
    seq_q_eci2body = seq_q_eci2body[:index]
    seq_nadir_body = seq_nadir_body[:,:index].transpose()
    seq_sun_position_eci = seq_sun_position_eci[:index]
    seq_sun_constant = seq_sun_constant[:index]
    sunlit = sunlit[:index]
    seq_power = [
        generate_power(q_eci2body, nadir_body, sun_position_eci.position.km, sun_constant)
        if is_lit else 0 for q_eci2body, nadir_body, sun_position_eci, sun_constant, is_lit
        in zip(seq_q_eci2body, seq_nadir_body, seq_sun_position_eci, seq_sun_constant, sunlit)
    ]

    with open(config.output_file, 'w') as file:
        file.write(str(seq_power))

    x = range(index)
    title = 'Comparison of Power Sequences'
    xlabel = 'Time Step'
    ylabel = 'Power Value'
    legend_labels = ['STK', 'Blender']
    plot_data(
        x,
        powers,
        seq_power,
        title,
        xlabel,
        ylabel,
        legend_labels,
        accumulate=False
    )
    print("hello")


if __name__ == "__main__":
    main()

# import ast
# def rr():
#     with open('our_power', 'r') as file:
#         seq_power_str = file.read()
#
#     return seq_power_str
#
# seq_power = ast.literal_eval(rr())
