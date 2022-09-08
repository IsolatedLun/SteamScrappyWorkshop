import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def load_config():
    with open(os.path.join(BASE_DIR, 'config.json'), 'r') as f:
        return json.load(f)

__CONFIG = load_config()

STEAM_URL = 'https://steamcommunity.com/sharedfiles/filedetails/?id='
STEAM_APP_URL = 'https://store.steampowered.com/app/'
VERSION = 1

STEAM_SEARCH_URL = 'https://steamcommunity.com/workshop/browse/?appid={0}&searchtext={1}&actualsort=trend&browsesort=trend&p=1&days=-1&p={2}'
STEAMCMD_WORKSHOP = ' +workshop_download_item {0} {1}'
STEAMCMD_LOGIN = 'steamcmd +login anonymous'

STEAMCMD_DIR = __CONFIG['steamcmd_dir']
ALIASES_DIR = os.path.join(BASE_DIR, 'aliases.json')

OUTPUT_IDENTIFIER = 'scrappyd'

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
        'prefixes': [],
        'help_text': ''
    },
    {
        'name': 'search',
        'args': [
            'App Alias', 'Query'
        ],
        'prefixes': [
            {
                'prefix': '--page',
                'help_text': 'Index'
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
        'prefixes': [
            {
                'prefix': '--add',
                'help_text': 'App Id'
            }
        ]
    },
    {
        'name': 'items',
        'help_text': 'Shows items',
        'args': [],
        'prefixes': [
            {
                'prefix': '--remove',
                'help_text': 'Index'
            }
        ]
    },
    {
        'name': '" "',
        'help_text': 'Use quotes => "God of war"',
        'args': [],
        'prefixes': []
    }
]
