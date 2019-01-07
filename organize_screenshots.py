import os
import json
from shutil import copy2
import requests

def list_images(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if "jpg" in name or "mp4" in name or "png" in name:
                r.append(os.path.join(root, name))
    return r

game_ids = json.loads(requests.get('https://raw.githubusercontent.com/RenanGreca/Switch-Screenshots/master/game_ids.json').text)

for image_location in list_images('.'):
    new_image_name = os.path.basename(image_location)
    game_id = image_location.split('-')[1].split('.')[0]

    if game_id in game_ids:
        game_name = game_ids[game_id]
        new_image_name = new_image_name.replace(game_id, game_name)

    copy2(image_location, new_image_name)
