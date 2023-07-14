import bpy
import numpy as np
from pyquaternion import Quaternion


def _get_object(name: str) -> bpy.types.Object:
    try:
        return bpy.data.objects[name]
    except KeyError:
        raise ValueError(f"'{name}' object not found in the current scene.")


def _get_image(name: str) -> bpy.types.Image:
    try:
        return bpy.data.images[name]
    except KeyError:
        raise ValueError(f"'{name}' image not found in the current scene.")


def get_cross_section(quaternion: Quaternion, pixels_per_m2: float) -> float:
    if pixels_per_m2 == 0:
        raise ValueError("pixels_per_m2 cannot be zero.")

    obj = _get_object("PeakSat v2")
    image = _get_image('Viewer Node')

    obj.rotation_quaternion = tuple(quaternion)
    bpy.ops.render.render(write_still=False)

    resolution_x = bpy.context.scene.render.resolution_x
    resolution_y = bpy.context.scene.render.resolution_y

    pixels = np.empty(resolution_x * resolution_y * 4, dtype=np.float32)
    image.pixels.foreach_get(pixels)

    pixels = pixels.reshape(resolution_x, resolution_y, 4)
    pixels = np.dot(pixels[..., :3], [0.299, 0.587, 0.114])  # RGB to grayscale

    white_pixels = np.sum(pixels > 3.5)

    return white_pixels / pixels_per_m2
