import json
import os
from pathlib import Path


def load_config():
    with open(os.path.join(BASE_DIR, 'config.json'), 'r') as f:
        return json.load(f)


STEAM_URL = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
STEAM_APP_URL = 'https://store.steampowered.com/app/'
VERSION = 1

STEAM_SEARCH_URL = 'https://steamcommunity.com/workshop/browse/?appid={0}&searchtext={1}&actualsort=trend&browsesort=trend&p=1&days=-1&p={2}'
STEAMCMD_WORKSHOP = ' +workshop_download_item {0} {1}'
STEAMCMD_LOGIN = 'steamcmd +login anonymous'

BASE_DIR = Path(__file__).resolve().parent.parent

STEAMCMD_DIR = load_config()['steamcmd_dir']
ALIASES_DIR = os.path.join(BASE_DIR, 'aliases.json')

COMMANDS = [
    {
        'name': 'download',
        'help_text': 'Runs Steamcmd on the file',
        'args': ['File Name'],
        'prefixes': []
    },
    {
        'name': 'collection',
        'args': [
            'App Alias', 'Collection Id'
        ],
        'prefixes': [
            {
                'prefix': '--download',
                'help_text': 'empty'
            }
        ],
        'help_text': ''
    },
    {
        'name': 'search',
        'args': [
            'App Alias', 'Query'
        ],
        'prefixes': [
            {
                'prefix': '--download',
                'help_text': 'empty'
            },
            {
                'prefix': '--page',
                'help_text': 'index'
            }
        ],
        'help_text': ''
    },
    {
        'name': 'output',
        'args': [],
        'prefixes': [
            {
                'prefix': '--out_dir',
                'help_text': 'location'
            }
        ],
        'help_text': ''
    },
    {
        'name': 'aliases',
        'help_text': 'Shows aliases',
        'args': [],
        'prefixes': []
    },
    {
        'name': '" "',
        'help_text': 'Use quotes => "God of war"',
        'args': [],
        'prefixes': []
    }
]
