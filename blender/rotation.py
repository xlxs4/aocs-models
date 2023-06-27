import numpy as np
from pyquaternion import Quaternion

def rotation_quaternion_from_vectors(vec1, vec2):
    """ Find the rotation quaternion that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return q: A unit quaternion which rotates vec1 to align with vec2.
    """
    vec1 = vec1 / np.linalg.norm(vec1)  # Unit vector along vec1
    vec2 = vec2 / np.linalg.norm(vec2)  # Unit vector along vec2
    cross_prod = np.cross(vec1, vec2)
    dot_prod = np.dot(vec1, vec2)
    q = Quaternion(axis=cross_prod, angle=np.arccos(dot_prod))  # Constructing the quaternion
    return q

# Given: v (replace vx, vy, vz with the actual coordinates of your vector)
v = np.array([1, 1, 1])  
v = v / np.linalg.norm(v)
r = np.array([1, 0, 0])

# Compute the rotation quaternion
rot_quaternion = rotation_quaternion_from_vectors(v, r)

# Apply the rotation quaternion to v
v_rotated = rot_quaternion.rotate(v)

print(f"The original vector v is {v}")
print(f"The rotation quaternion is {rot_quaternion}")
print(f"The rotated vector v_rotated is {v_rotated}")
