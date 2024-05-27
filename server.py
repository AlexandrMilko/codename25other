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
    obj_path = os.path.abspath(data['model_path'])
    render_path = os.path.abspath('render.png')

    blender_cmd = [
        "blender",
        "--background",
        "--python",
        blender_script_path,
        "--",
        json.dumps(data['obj_angles']),
        json.dumps(data['obj_scale']),
        json.dumps(data['obj_offsets']),
        json.dumps(data['camera_angles']),
        json.dumps(data['camera_location']),
        json.dumps(data['resolution_x']),
        json.dumps(data['resolution_y']),
        obj_path,
        render_path
    ]

    subprocess.run(blender_cmd, check=True)

    with open(render_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    return jsonify({'image_base64': encoded_string})


if __name__ == "__main__":
    app.run(port=5002)
