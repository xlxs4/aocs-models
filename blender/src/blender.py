import bpy
import numpy as np


def get_cross_section(quaternion):
    pixels_per_m2 = 264921.8466012359

    bpy.data.objects["PeakSat v2"].rotation_quaternion = tuple(quaternion)
    
    # Render the scene
    bpy.ops.render.render(write_still=False)

    # copy buffer to numpy array for faster manipulation
    arr = np.array(bpy.data.images['Viewer Node'].pixels)
    image = arr.reshape(
        bpy.context.scene.render.resolution_x,
        bpy.context.scene.render.resolution_y, 4
    )

    image = np.dot(image[..., :3], [0.299, 0.587, 0.114])
    
    # Binarize the image using a threshold of 0.5
    pixels_array_bin = image > 3.5

    # Count the white pixels (pixels over threshold)
    white_pixels = np.sum(pixels_array_bin)

    return white_pixels / pixels_per_m2
