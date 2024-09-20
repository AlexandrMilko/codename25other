import requests
import cv2
import base64
import os
import time

def save_encoded_image(b64_image: str, output_path: str):
    """
    Save the given image to the given output path.
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))


def get_encoded_image(image_path):
    """
    Read and encode the image from the given path into base64.
    """
    img = cv2.imread(image_path)
    # Encode into PNG and send to ControlNet
    retval, bytes_img = cv2.imencode('.png', img)
    return base64.b64encode(bytes_img).decode('utf-8')


def process_images_in_directory(input_dir, output_dir):
    """
    Process all images in the given directory and save results with 'after' in their filename.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # URL of the Flask app
    url = 'http://127.0.0.1:5000/ai/get_insane_image_1337'

    # Iterate through all image files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(input_dir, filename)

            # Prepare data for the API call
            data = {
                'room_choice': 'bedroom',
                'style_budget_choice': 'Scandinavian, High-End',
                'input_image': get_encoded_image(image_path)
            }

            # Sending POST request to the Flask app
            response = requests.post(url, json=data)

            # Check if the request was successful
            if response.status_code == 200:
                print(f"Processing {filename} - Done")
                # Create the output filename by appending 'after' before the extension
                base_name, ext = os.path.splitext(filename)
                output_filename = f"{base_name}_after{ext}"
                output_path = os.path.join(output_dir, output_filename)
                # Save the encoded image to the output directory
                save_encoded_image(response.json()['output_image'], output_path)
            else:
                print(f"Failed to process {filename}. Status code: {response.status_code}")
            time.sleep(30)

if __name__ == '__main__':
    input_directory = '/home/stage/Desktop/testphotos'
    output_directory = '/home/stage/Desktop/testphotos'
    process_images_in_directory(input_directory, output_directory)
