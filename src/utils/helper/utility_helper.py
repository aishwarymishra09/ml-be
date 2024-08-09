import json
import os
import shutil
import uuid
import websocket
from PIL import Image
import io
from src.utils.constants.properties import REMOTE_IMAGE_FILE, GARMENT, MODEL
from src.utils.helper.comfy_helper import get_images
from src.utils.helper.s3_helper import download_s3_file, save_image, download_image_from_s3

server_address = "216.48.187.54:8188"



def download_files(uid, s3_path, model_path):

    # Create directories if they don't exist
    local_path = os.getcwd() + f"/{uid}/"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    _, garment_path = download_image_from_s3(s3_path, local_path)
    _, model_path2 = download_image_from_s3(model_path, local_path)

    return garment_path[0], model_path2[0], local_path


def model_cloth_swap(uid, prompt, model_path, s3_path):
    """This function is used to swap the cloth of the model """
    client_id = str(uuid.uuid4())
    with open('src/training_scripts/cloths_final.json', 'r') as file:
        data = json.load(file)
    garment_path, model_path, local_path = download_files(uid, s3_path, model_path)
    # set the text prompt for our positive CLIPTextEncode
    data["12"]["inputs"]["prompt"] = prompt

    # set the seed for our KSampler node
    data["13"]["inputs"]["image"] = garment_path
    data["14"]["inputs"]["image"] = model_path

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, data, client_id, server_address)

    #img_path = REMOTE_IMAGE_FILE.format("fashion", uid, 1)
    # Commented out code to display the output images:
    img_path = REMOTE_IMAGE_FILE.format("fashion", uid, 1)
    for node_id in images:
        for image_data in images[node_id]:
            if node_id == '20':
                image = Image.open(io.BytesIO(image_data))
                # image.save("{}.png".format(node_id + 'a'))
                save_image(image, "infernce-rekogniz/fashion" + f"/{uid}" + "/sample_1.png")

    shutil.rmtree(local_path)
    return img_path


def custom_bg(uid, image_path, product_prompt,superimpose, prompt_bg):
    """This function is used to change the background of the images"""
    client_id = str(uuid.uuid4())
    with open('src/training_scripts/aa.json', 'r') as file:
        data = json.load(file)
    local_path = os.getcwd() + f"/{uid}/"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    _, product_path = download_image_from_s3(image_path, local_path)
    data["92"]["inputs"]["Text"] = prompt_bg
    data["97"]["inputs"]["Text"] = product_prompt

    # set the seed for our KSampler node
    data["4"]["inputs"]["image"] = product_path[0]

    #######################################################

    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, data, client_id, server_address)

    #img_path = REMOTE_IMAGE_FILE.format("bg", uid, 1)
    # Commented out code to display the output images:
    img_path = REMOTE_IMAGE_FILE.format("bg", uid, 1)
    for node_id in images:

        for image_data in images[node_id]:
            if node_id == '100':
                image = Image.open(io.BytesIO(image_data))
                if superimpose:
                    superimpose_bg()

                save_image(image, "infernce-rekogniz/bg" + f"/{uid}" + f"/sample_1.png")
                # image.save("{}.png".format(node_id + 'bg'))
    shutil.rmtree(local_path)
    return img_path

def superimpose_bg(input_image, generated_image):
    """This function is used to change the background of the images"""
    client_id = str(uuid.uuid4())
    with open('src/training_scripts/aa.json', 'r') as file:
        data = json.load(file)

    data['106']['inputs']['image'] = input_image
    data['107']['inputs']['image'] = generated_image
    ws = websocket.WebSocket()
    ws.connect("ws://{}/ws?clientId={}".format(server_address, client_id))
    images = get_images(ws, data, client_id, server_address)

    return images["109"]