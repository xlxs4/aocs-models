import bpy
import numpy as np
from pyquaternion import Quaternion

from config import config


def _rgb_to_grayscale(image: np.ndarray) -> np.ndarray:
    return np.dot(image[..., :3], [0.299, 0.587, 0.114])


def get_cross_section(quaternion: Quaternion) -> float:
    obj = bpy.data.objects[config.blender_obj_name]
    image = bpy.data.images['Viewer Node']

    obj.rotation_quaternion = tuple(quaternion)
    bpy.ops.render.render(write_still=False)

    resolution_x = bpy.context.scene.render.resolution_x
    resolution_y = bpy.context.scene.render.resolution_y

    # Working on a local copy of the pixels results in huge performance improvement.
    # Additionally, instead of directly accessing pixels, we use foreach, introduced in
    # https://projects.blender.org/blender/blender/commit/9075ec8269e7cb029f4fab6c1289eb2f1ae2858a
    # and discussed in https://devtalk.blender.org/t/bpy-data-images-perf-issues/6459/11
    pixels = np.empty(resolution_x * resolution_y * 4, dtype=np.float32)
    image.pixels.foreach_get(pixels)

    pixels = pixels.reshape(resolution_x, resolution_y, 4)
    pixels = _rgb_to_grayscale(pixels)

    white_pixels = np.sum(pixels > 3.5)

    return white_pixels / config.pixels_per_m2
