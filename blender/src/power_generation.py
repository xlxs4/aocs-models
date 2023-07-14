import itertools
import math
from typing import List

import bpy
import matplotlib.pyplot as plt
import numpy as np
from astropy.time import Time
from skyfield.api import load
from skyfield.jpllib import SpiceKernel
from skyfield.positionlib import ICRF

import parse
from blender import get_cross_section
from config import config
from utils import align_with_sun_and_nadir


def generate_power(
    q_eci2body: np.ndarray, nadir_body: np.ndarray,
    sun_position_eci_km: np.ndarray, sun_constant: float
) -> float:
    sun_eci = sun_position_eci_km / np.linalg.norm(sun_position_eci_km)
    sun_eci = sun_eci / np.linalg.norm(sun_eci)
    sun_body = q_eci2body.conjugate.rotate(sun_eci)
    nadir_body = nadir_body / np.linalg.norm(nadir_body)
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


def get_sun_position(eph: SpiceKernel, t: List) -> ICRF:
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
    t_jd, seq_q_eci2body, _, powers, = parse.parse_data()

    bpy.ops.wm.open_mainfile(filepath=config.paths.blender_model)

    bpy.data.objects[config.blender_obj_name].rotation_mode = 'QUATERNION'
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    # create input render layer node
    rl = tree.nodes.new('CompositorNodeRLayers')
    rl.location = 185, 285

    # create output node
    v = tree.nodes.new('CompositorNodeViewer')
    v.location = 750, 210
    v.use_alpha = False

    links.new(rl.outputs[0], v.inputs[0])

    bpy.context.scene.render.resolution_x = 400
    bpy.context.scene.render.resolution_y = 400

    eph = load(config.paths.ephemeris)
    t = get_time_sequence(t_jd)

    seq_sun_position_eci = get_sun_position(eph, t)

    satellites = load.tle_file(config.paths.tle)
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name['ISS (ZARYA)']
    geocentric_position = satellite.at(t)
    # 'up' vector is simply the negation of the position, as the vector from satellite to Earth's center
    seq_nadir_body = -geocentric_position.position.km.transpose()
    sunlit = satellite.at(t).is_sunlit(eph)

    seq_sun_constant = [get_sun_constant(time.tt) for time in t]

    seq_power = [
        generate_power(
            q_eci2body, nadir_body, sun_position_eci.position.km, sun_constant
        ) if is_lit else 0 for q_eci2body, nadir_body, sun_position_eci,
        sun_constant, is_lit in zip(
            seq_q_eci2body, seq_nadir_body, seq_sun_position_eci,
            seq_sun_constant, sunlit
        )
    ]

    x = range(len(powers))
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
        accumulate=True
    )


if __name__ == "__main__":
    main()
