import os
import json
from shutil import copy2
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default='.', help='path to operate on')
parser.add_argument('--delete', action='store_true', help='delete original files after organizing')
args = parser.parse_args()

def list_images(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            if "jpg" in name or "mp4" in name or "png" in name:
                r.append(os.path.join(root, name))
    return r

game_ids = json.loads(requests.get('https://raw.githubusercontent.com/RenanGreca/Switch-Screenshots/master/game_ids.json').text)

image_list = list_images(os.path.join(args.path, 'input'))

for image_location in image_list:
    new_image_name = os.path.basename(image_location)
    game_id = image_location.split('-')[1].split('.')[0]

    if game_id in game_ids:
        game_name = game_ids[game_id]
        new_image_name = new_image_name.replace(game_id, game_name)

    new_location = os.path.join(args.path, new_image_name)
    if not os.path.exists(new_location):
        copy2(image_location, new_location)

if args.delete:
    for old_file_location in image_list:
        os.remove(old_file_location)

    for root, directories, filenames in os.walk(os.path.join(args.path, 'input'), topdown=False):
        for directory in directories:
            directory_path = os.path.join(root, directory)
            if len(os.listdir(directory_path)) == 0:
                os.rmdir(directory_path)
