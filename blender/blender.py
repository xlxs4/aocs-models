import bpy
import numpy as np
from PIL import Image
import os
import tempfile
from math import radians
import matplotlib.pyplot as plot

# Specify the path to your .blend file
filepath = "model.blend"

# Load the .blend file
bpy.ops.wm.open_mainfile(filepath=filepath)

# Specify the rotation angles in degrees
rotation_angles = (45, 30, 0)  # rotation in X, Y, Z directions

# Convert the rotation angles to radians (Blender uses radians for rotation)
rotation_angles_rad = [radians(angle) for angle in rotation_angles]

bpy.data.objects["PeakSat v2"].rotation_euler = rotation_angles_rad

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

    plot.imshow(pixels_array_bin)
    plot.show()

    # Count the white pixels (pixels over threshold)
    white_pixels = np.sum(pixels_array_bin)

    print('Number of white pixels:', white_pixels)

finally:
    # Clean up the temporary file
    os.close(fd)
    os.remove(path)
