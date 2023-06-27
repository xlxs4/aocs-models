import bpy
import numpy as np
from PIL import Image
import os
import tempfile


def get_cross_section(quaternion):
    # Specify the path to your .blend file
    filepath = "../model/model.blend"

    pixels_per_m2 = 509953.9170506912

    # Load the .blend file
    bpy.ops.wm.open_mainfile(filepath=filepath)

    bpy.data.objects["PeakSat v2"].rotation_quaternion = list(quaternion)

    # Specify the output path for the rendered image
    bpy.context.scene.render.filepath = "render.png"

    # Set output format to PNG
    bpy.context.scene.render.image_settings.file_format = 'PNG'

    # Specify render resolution
    bpy.context.scene.render.resolution_x = 400
    bpy.context.scene.render.resolution_y = 400

    # Render the scene
    bpy.ops.render.render(write_still=True)

    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix=".png")

    try:
        # Save the rendered image to the temporary file
        bpy.data.images['Render Result'].save_render(filepath=path)

        # Open the image file
        img = Image.open(path)

        # Convert the image data to a numpy array
        pixels_array = np.array(img)

        # Binarize the image using a threshold of 0.5
        pixels_array_bin = pixels_array > 100

        # Count the white pixels (pixels over threshold)
        white_pixels = np.sum(pixels_array_bin)
        cross_sectional_area = white_pixels / pixels_per_m2

    finally:
        # Clean up the temporary file
        os.close(fd)
        os.remove(path)

    return cross_sectional_area
