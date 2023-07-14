import numpy as np
from pyquaternion import Quaternion
from scipy.spatial.transform import Rotation as R


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
