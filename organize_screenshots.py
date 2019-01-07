# Renan Greca, 2017
# This code is free to distribute and alter.

# Place this script in the same directory as the Switch's Album folder.
# View README.md for more details.

import os
import json
from shutil import copy2
import requests

# Create a list of all the image files in the Album directory.
# Thanks to L. Teder
# https://stackoverflow.com/a/36898903
def list_images(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if "jpg" in name or "mp4" in name or "png" in name:
                r.append(os.path.join(root, name))
    return r

# Load game IDs file
game_ids = json.loads(requests.get('https://raw.githubusercontent.com/RenanGreca/Switch-Screenshots/master/game_ids.json').text)

# Iterate over images
for image in list_images('Album'):
    image_id = image.split('-')[1].split('.')[0]

    if not os.path.exists('Output'):
        os.makedirs('Output')

    # If the ID was in the JSON file, create a directory and copy the file
    if image_id in game_ids:
        game_title = game_ids[image_id]
        path = os.path.join('Output', game_title)
        if not os.path.exists(path):
            os.makedirs(path)
        copy2(image, path)
    else:
        print("Game ID not found for image", image)
