import json
import os
from pathlib import Path


def load_config():
    with open(os.path.join(BASE_DIR, 'config.json'), 'r') as f:
        return json.load(f)


STEAM_URL = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
STEAM_APP_URL = 'https://store.steampowered.com/app/'
VERSION = 1

STEAM_SEARCH_URL = 'https://steamcommunity.com/workshop/browse/?appid={0}&searchtext={1}&actualsort=trend&browsesort=trend&p=1&days=-1'
STEAMCMD_WORKSHOP = ' +workshop_download_item {0} {1}'
STEAMCMD_LOGIN = 'steamcmd +login anonymous'

BASE_DIR = Path(__file__).resolve().parent.parent

STEAMCMD_DIR = load_config()['steamcmd_dir']
ALIASES_DIR = os.path.join(BASE_DIR, 'aliases.json')
