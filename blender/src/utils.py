import numpy as np
from pyquaternion import Quaternion
from scipy.spatial.transform import Rotation as R


def align_with_sun_and_nadir(v1, v2):
    # Normalize the vectors
    v1 = v1 / np.linalg.norm(v1)  # Sun vector
    v2 = v2 / np.linalg.norm(v2)  # Nadir vector

    # Calculate the satellite body frame
    x_sat = -v1
    y_sat = v2 - v1 * np.dot(
        v1, v2
    )  # remove the component of v2 that is in the direction of v1
    y_sat = y_sat / np.linalg.norm(
        y_sat
    )  # normalize again after the subtraction
    z_sat = np.cross(x_sat, y_sat)
    z_sat = z_sat / np.linalg.norm(
        z_sat
    )  # z is now perpendicular to both x (v1) and y

    # Form the rotation matrix
    rotation_matrix = np.vstack((x_sat, y_sat, z_sat))

    # Convert the rotation matrix to a quaternion
    rotation = R.from_matrix(rotation_matrix)

    quat = rotation.as_quat()

    return Quaternion([quat[3], quat[0], quat[1], quat[2]])
