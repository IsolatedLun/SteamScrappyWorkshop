# =========================
# Printing functions
# =========================
import os
from random import random

from src.consts import (COMMANDS, DASH_LENGTH)


def show_welcome(v: int):
    print(
        f"""
SteamScrappyDownloader v{v}
______________________
{show_help()}
""")


def show_help():
    return \
        f"""
COMMANDS:
------------------------------------
{create_help_commands(COMMANDS)}
------------------------------------
"""


def show_items(_items: list[dict]):
    res = ''
    i = 0

    for item_name in _items.keys():
        (app_id, name, id, sanitized_name, *_) = * \
            _items[item_name].values(), item_name
        res += f'| {name} => {id} [{sanitized_name}]'
        res += '\n' + ('-' * DASH_LENGTH // 2) + '\n'

        i += 1

    return res, i


def create_help_commands(commands: list[dict]):
    command_list = [
        ['Command', 'Help', 'Arguments', 'Prefixes'],
        ['--------', '-----', '----------', '---------']
    ]
    for i, command in enumerate(commands):
        args = ''
        prefixes = ''

        for arg in command['args']:
            args += f'<{arg}> '
        for prefix in command['prefixes']:
            prefixes += f'{prefix["prefix"]}({prefix["help_text"]}) '

        command_list.append([
            command['name'], command['help_text'], args, prefixes
        ])

    table = create_even_table(
        command_list
    )

    return table

# =========================
# Command functions
# =========================


def get_arg_index(commands: list[str], command):
    res = commands.index(command) + 1

    if res > len(commands) - 1:
        raise Exception(
            f'Invalid parameters: "{command}" must have an value after it')
    else:
        return res

# =========================
# Text functions
# =========================


def sanitize_text(text: str):
    return '-'.join([x.replace('-', '') for x in text.split(' ')]).lower() \
        .replace("'", '').replace('—', '') \
        .replace('[', '').replace(']', '') \
        .replace('"', '')


def clean_quotes(text: str):
    return text.replace('"', '')

def clean_newlines(text: str):
    return text.replace('\n', '')

# =========================
# File functions
# =========================


def read_output_file(path: str):
    if os.path.exists(path):
        with open(path, 'r') as f:
            f.seek(0)

            return f.read()
    else:
        raise Exception(f'> File at "{path}" does not exist')

# =========================
# Misc functions
# =========================


def create_random_char(_len: int):
    def ch_code():
        return (random() * 24).__ceil__()

    res = ''
    while _len:
        res += chr(65 + ch_code())
        _len -= 1
    return res


def create_even_table(rows: list[str]):
    widths = [max(map(len, col)) for col in zip(*rows)]
    table = ''

    for row in rows:
        table += '   '.join((val.ljust(width)
                             for val, width in zip(row, widths))) + '\n'
    return table

def sub_str(x: str, to_search: str):
    i = 0

    if len(to_search) > len(x):
        return False

    while i < len(x):
        if to_search == x[i:i + len(to_search)]:
            return True
        
        i += 1
    return False

def count_sub_str(x: str, to_search: str):
    i, j = 0, 0

    if len(to_search) > len(x):
        return 0

    while j < len(x):
        if to_search == x[j:j + len(to_search)]:
            i += 1
        j += 1
    return i