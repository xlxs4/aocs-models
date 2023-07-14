import bpy
import numpy as np


def get_cross_section(quaternion, pixels_per_m2):
    bpy.data.objects["PeakSat v2"].rotation_quaternion = tuple(quaternion)

    bpy.ops.render.render(write_still=False)

    # Working on a local copy of the pixels results in huge performance improvement.
    # Additionally, instead of directly accessing pixels, we use foreach, introduced in
    # https://projects.blender.org/blender/blender/commit/9075ec8269e7cb029f4fab6c1289eb2f1ae2858a
    # and discussed in https://devtalk.blender.org/t/bpy-data-images-perf-issues/6459/11
    pixels = np.empty(
        bpy.context.scene.render.resolution_x *
        bpy.context.scene.render.resolution_y * 4,
        dtype=np.float32
    )
    bpy.data.images['Viewer Node'].pixels.foreach_get(pixels)
    pixels = pixels.reshape(
        bpy.context.scene.render.resolution_x,
        bpy.context.scene.render.resolution_y, 4
    )

    pixels = np.dot(pixels[..., :3], [0.299, 0.587, 0.114])

    # Binarize the image
    pixels_array_bin = pixels > 3.5
    white_pixels = np.sum(pixels_array_bin)

    return white_pixels / pixels_per_m2
