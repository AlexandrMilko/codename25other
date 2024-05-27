import json
import sys
import bpy


def setup_camera(angles, location):
    # Get the current scene
    scene = bpy.context.scene

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
    scene = bpy.context.scene
    # Add a point light
    light_data = bpy.data.lights.new(name='PointLight', type='POINT')
    light_obj = bpy.data.objects.new(name='PointLight', object_data=light_data)
    scene.collection.objects.link(light_obj)
    light_obj.location = (2, 2, 5)
    light_data.energy = 1000.0
    light_data.color = (1, 1, 1)


def add_obj_model(obj_path, location, angles, scale):
    scene = bpy.context.scene
    # Load your .obj model with the updated operator
    bpy.ops.import_scene.obj(filepath=obj_path)
    # Assuming your .obj model is imported as the active object
    imported_objs = bpy.context.selected_objects
    # Create an Empty object to act as the parent
    furniture = bpy.data.objects.new("Furniture", None)
    scene.collection.objects.link(furniture)

    # Parent all the imported objects to the Empty object
    for obj in imported_objs:
        obj.parent = furniture

    furniture.location = location
    furniture.rotation_euler = angles
    furniture.scale = scale


def save_render(path, resolution_x, resolution_y):
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'PNG'
    # Set color mode to RGBA for alpha channel
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.filepath = path
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    # Enable transparent background
    scene.render.film_transparent = True
    # Render the scene
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    # Select all default objects in the scene
    bpy.ops.object.select_all(action='SELECT')

    # Delete all default selected objects
    bpy.ops.object.delete()

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

    setup_camera(camera_angles, camera_location)
    setup_light()
    add_obj_model(obj_path, obj_offsets, obj_angles, obj_scale)
    save_render(render_path, resolution_x, resolution_y)
