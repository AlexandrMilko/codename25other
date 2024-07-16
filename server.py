from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import base64
import json
import os

app = Flask(__name__)
CORS(app)


@app.route('/render_image', methods=['POST'])
def render_image():
    data = request.json
    blender_script_path = os.path.abspath('blender_script.py')
    render_path = os.path.abspath('visuals/render.png')
    blend_file_path = os.path.abspath('visuals/scene.blend')

    blender_cmd = [
        "/Applications/Blender.app/Contents/MacOS/Blender",
        "--background",
        "--python",
        blender_script_path,
        "--",
        json.dumps({
            "render_path": render_path,
            "blend_file_path": blend_file_path,
            "camera_location": data['camera_location'],
            "camera_angles": data['camera_angles'],
            "resolution_x": data['resolution_x'],
            "resolution_y": data['resolution_y'],
            "objects": data['objects']
        })
    ]

    subprocess.run(blender_cmd, check=True)

    with open(render_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({'image_base64': encoded_string})


if __name__ == "__main__":
    app.run(port=5002)
