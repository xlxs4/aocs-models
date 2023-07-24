import bpy
from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite
from eltypes import Time
import parse
from config import config
from generation import generate_power
from utils import plot_data, sun_constant, sun_position, time_sequence, orbital_elements_to_tle


def main(should_plot: bool = False):
    t_jd, seq_q_eci2body, _, powers, = parse.parse_data()

    bpy.ops.wm.open_mainfile(filepath=config.paths.blender_model)

    bpy.data.objects[config.blender_obj_name].rotation_mode = 'QUATERNION'
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    # Create input render layer node
    rl = tree.nodes.new('CompositorNodeRLayers')
    rl.location = 185, 285

    # Create output node
    v = tree.nodes.new('CompositorNodeViewer')
    v.location = 750, 210
    v.use_alpha = False

    links.new(rl.outputs[0], v.inputs[0])

    bpy.context.scene.render.resolution_x = config.blender_res_x
    bpy.context.scene.render.resolution_y = config.blender_res_y

    eph = load(config.paths.ephemeris)
    t = time_sequence(t_jd)

    seq_sun_position_eci = sun_position(eph, t)

    # Orbital parameters
    a = 6871  # Semi-major axis in km
    e = 0.001  # Eccentricity
    i = 51.65  # Inclination in degrees
    raan = 0  # Right ascension of the ascending node in degrees
    argp = 0  # Argument of perigee in degrees
    nu = 0  # True anomaly in degrees
    
    epoch = Time(t[0].tt, format='jd')

    # Get TLE lines
    line1, line2 = orbital_elements_to_tle(a, e, i, raan, argp, nu, epoch)

    # Create an EarthSatellite object
    satellite = EarthSatellite(line1, line2, name='My Satellite')
    # satellites = load.tle_file(config.paths.tle)
    # by_name = {sat.name: sat for sat in satellites}
    # satellite = by_name['ISS (ZARYA)']
    geocentric_position = satellite.at(t)
    # 'up' vector is simply the negation of the position, as the vector from satellite to Earth's center
    seq_nadir_body = -geocentric_position.position.km.transpose()
    sunlit = satellite.at(t).is_sunlit(eph)

    seq_sun_constant = [sun_constant(time.tt) for time in t]

    seq_power = [
        generate_power(
            q_eci2body, nadir_body, sun_position_eci.position.km, sun_constant
        ) if is_lit else 0 for q_eci2body, nadir_body, sun_position_eci,
        sun_constant, is_lit in zip(
            seq_q_eci2body, seq_nadir_body, seq_sun_position_eci,
            seq_sun_constant, sunlit
        )
    ]

    if should_plot:
        plot_data(
            range(len(powers)),
            powers,
            seq_power,
            config.plot_title,
            config.plot_xlabel,
            config.plot_ylabel,
            config.plot_legend_labels,
            accumulate=True
        )


if __name__ == "__main__":
    main(should_plot=True)
