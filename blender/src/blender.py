import bpy
import numpy as np
from PIL import Image


def get_cross_section(quaternion):
    # FIXME
    pixels_per_m2 = 509953.9170506912

    bpy.data.objects["PeakSat v2"].rotation_mode = 'QUATERNION'
    bpy.data.objects["PeakSat v2"].rotation_quaternion = tuple(quaternion)

    # switch on nodes
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    links = tree.links

    # create input render layer node
    rl = tree.nodes.new('CompositorNodeRLayers')
    rl.location = 185, 285

    # create output node
    v = tree.nodes.new('CompositorNodeViewer')
    v.location = 750, 210
    v.use_alpha = False

    # Links
    links.new(rl.outputs[0], v.inputs[0])  # link Image output to Viewer input

    # Specify render resolution
    bpy.context.scene.render.resolution_x = 400
    bpy.context.scene.render.resolution_y = 400

    # Render the scene
    bpy.ops.render.render(write_still=False)

    # copy buffer to numpy array for faster manipulation
    arr = np.array(bpy.data.images['Viewer Node'].pixels)
    image = arr.reshape(400, 400, 4)
    image = np.dot(image[..., :3], [0.299, 0.587, 0.114])

    # Binarize the image using a threshold of 0.5
    pixels_array_bin = image > 3.5

    # Count the white pixels (pixels over threshold)
    white_pixels = np.sum(pixels_array_bin)

    return white_pixels / pixels_per_m2
