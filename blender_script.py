import json
import sys
import bpy


def open_blend_file(filepath):
    bpy.ops.wm.open_mainfile(filepath=filepath)


def setup_camera(angles, location):
    # Create a new camera object
    cam_data = bpy.data.cameras.new(name='Camera')
    cam_obj = bpy.data.objects.new('Camera', cam_data)

    # Link the camera to the scene
    scene.collection.objects.link(cam_obj)

    # Set the camera's location and rotation
    cam_obj.location = location
    cam_obj.rotation_euler = angles
    cam_obj.data.lens = 20
    scene.camera = cam_obj


def setup_light():
    # Create light data and object
    light_data = bpy.data.lights.new(name='PointLight', type='POINT')
    light_obj = bpy.data.objects.new(name='PointLight', object_data=light_data)

    # Link light object to the scene
    scene.collection.objects.link(light_obj)

    # Set light location, intensity, and color
    light_obj.location = (2, 2, 5)
    light_data.energy = 1000.0
    light_data.color = (1, 1, 1)


def save_render(path, resolution_x, resolution_y):
    # Set render settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.filepath = path
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.film_transparent = True

    # Render the scene
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    # Parse command-line arguments
    args = sys.argv[sys.argv.index("--") + 1:]
    obj_angles = json.loads(args[0])
    obj_scale = json.loads(args[1])
    obj_offsets = json.loads(args[2])
    camera_angles = json.loads(args[3])
    camera_location = json.loads(args[4])
    resolution_x = json.loads(args[5])
    resolution_y = json.loads(args[6])
    blend_file_path = args[7]
    render_path = args[8]

    print("I START RENDERING WITH FOLLOWING SETTINGS: ")
    print(f"obj_angles = {obj_angles}")
    print(f"obj_scale = {obj_scale}")
    print(f"obj_offsets = {obj_offsets}")
    print(f"camera_angles = {camera_angles}")
    print(f"camera_location = {camera_location}")
    print(f"resolution_x = {resolution_x}")
    print(f"resolution_y = {resolution_y}")
    print(f"blend_file_path = {blend_file_path}")
    print(f"render_path = {render_path}")

    # Open the .blend file
    open_blend_file(blend_file_path)

    # Get the current scene
    scene = bpy.context.scene

    # Setup camera and light in the opened .blend file scene
    setup_camera(camera_angles, camera_location)
    setup_light()

    # Save the render with specified settings
    save_render(render_path, resolution_x, resolution_y)
