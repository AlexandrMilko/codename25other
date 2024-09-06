import requests
import cv2
import base64


def save_encoded_image(b64_image: str, output_path: str):
    """
    Save the given image to the given output path.
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))


def get_encoded_image(image_path):
    img = cv2.imread(image_path)
    # Encode into PNG and send to ControlNet
    retval, bytes = cv2.imencode('.png', img)
    return base64.b64encode(bytes).decode('utf-8')


def test_api():
    # URL of the Flask app
    url = 'http://127.0.0.1:5000/ai/get_insane_image_1337'

    # JSON data to send in the POST request
    data = {
        'room_choice': 'bedroom',
        'style_budget_choice': 'Contemporary, High-End',
        'input_image': get_encoded_image('/home/stage/Desktop/results_bedroom/2_empty.jpg')
    }

    # Sending POST request to the Flask app
    response = requests.post(url, json=data)

    # Printing the response text
    if response.status_code == 200:
        print('Done')
    else:
        print('Failed to get response. Status code:', response.status_code)
    save_encoded_image(response.json()['output_image'], 'visuals/after.jpg')


if __name__ == '__main__':
    test_api()
