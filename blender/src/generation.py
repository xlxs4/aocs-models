import numpy as np

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
