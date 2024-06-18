import json
import sys
import bpy


def setup_camera(angles, location):
    # Create a new camera object
    cam_data = bpy.data.cameras.new(name='Camera')
    cam_obj = bpy.data.objects.new('Camera', cam_data)

    # Link the camera to the scene
    scene.collection.objects.link(cam_obj)

    # Set the camera's location and rotation
    cam_obj.location = location
    cam_obj.rotation_euler = angles
    cam_obj.data.lens = 14
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


def add_3d_model(path, location, angles, scale):
    # Import the 3D model
    bpy.ops.wm.usd_import(filepath=path)

    # Get the imported objects
    imported_objs = bpy.context.selected_objects

    # Create and link an empty parent object
    furniture = bpy.data.objects.new("Furniture", None)
    scene.collection.objects.link(furniture)

    # Parent imported objects to the empty object
    for obj in imported_objs:
        obj.parent = furniture

    # Set location, rotation, and scale
    furniture.location = location
    furniture.rotation_euler = angles
    furniture.scale = scale


def save_render(path, res_x, res_y):
    # Set render settings
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.filepath = path
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
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
    obj_path = args[7]
    render_path = args[8]

    print("I START RENDERING WITH FOLLOWING SETTINGS: ")
    print(f"obj_angles = {obj_angles}")
    print(f"obj_scale = {obj_scale}")
    print(f"obj_offsets = {obj_offsets}")
    print(f"camera_angles = {camera_angles}")
    print(f"camera_location = {camera_location}")
    print(f"resolution_x = {resolution_x}")
    print(f"resolution_y = {resolution_y}")
    print(f"obj_path = {obj_path}")
    print(f"render_path = {render_path}")

    # Select and delete all default objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Get current scene, add camera/light, import model, and render
    scene = bpy.context.scene

    setup_camera(camera_angles, camera_location)
    setup_light()

    add_3d_model(obj_path, obj_offsets, obj_angles, obj_scale)

    save_render(render_path, resolution_x, resolution_y)
