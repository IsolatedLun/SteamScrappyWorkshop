# =========================
# Printing functions
# =========================
import os
from random import random

from src.consts import (BASE_DIR, COMMANDS, OUTPUT_IDENTIFIER, STEAMCMD_LOGIN, load_config)


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
        res += '\n' + ('-' * 18) + '\n'

        i += 1

    return res, i


def create_help_commands(commands: list[dict]):
    def with_sep(text, sep='|'):
        return text + ' ' + sep if text else ''

    res = ''
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
# Writing functions
# =========================


def output_commands(out: str, options: list[str], *vars: list[str]):
    """
        Creates an output text file that contains the command to donwload the items with steamcmd
    """
    def fix_out_dir(out_dir: str):
        """
            Appends the [scrappyd] identifier at the end of the text file's name 
        """
        temp = out_dir

        if out_dir.endswith('.txt'):
            temp = out_dir[0:len(out_dir) - 4]
        
        if not sub_str(out_dir, f'[{OUTPUT_IDENTIFIER}]'):
            temp += f'[{OUTPUT_IDENTIFIER}]'
        temp += '.txt'

        return temp

    def generate_file_name(vars: list[str]):
        return '-'.join(vars) + f'-{create_random_char(3)}'

    config = load_config()
    out_dir = ''
    has_multiple_params = False

    if '--dir' in options:
        idx = get_arg_index(options, '--dir')

        if not len(options) > idx + 1:
            out_dir = clean_quotes(options[idx])
        else:
            has_multiple_params = True

    # If the user hasn't specified the output in the cli and there is an out_dir in the config
    if not out_dir and config['out_dir'] and has_multiple_params:
        options.remove('--dir') # This is removed since it's useless

        if len(options) > count_sub_str(config['out_dir'], '{}'):
            raise Exception('Too many parameters for output directory')

        fname = ''
        if len(options) == 0:
            fname = generate_file_name(vars)
        else:
            fname = generate_file_name(vars) if options[-1] == '*'  else generate_file_name(options[-1])
            try:
                options.remove('*') # This is removed to avoid invalid argument errors
            except:
                pass

        out_dir = config['out_dir'].format(*options, fname)
    elif not out_dir and config['out_dir']:
        root_dir = config['out_dir'].split('/')[0]
        out_dir = os.path.join(root_dir, generate_file_name(vars))
    elif not out_dir:
        out_dir = generate_file_name(vars)

    # After creating the out_dir, we append the [scrappyd] string to the file name, so that we can access it later
    # This makes sure that the program only interacts with files that have [scrappyd] in their names.
    # Preventing accidential overrides/deletions of other non-related files
    out_dir = fix_out_dir(os.path.join(BASE_DIR, out_dir))

    os.makedirs(os.path.dirname(out_dir), exist_ok=True)
    with open(out_dir, config['mode']) as f:
        f.seek(0)  # goto the 1st line

        data = f.readline()

        if data.startswith('steamcmd'):
            f.write(out)
        else:
            f.write(STEAMCMD_LOGIN + out)
    return out_dir

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

# =========================
# File functions
# =========================


def read_output_file(path: str):
    if os.path.exists(path):
        with open(path, 'r') as f:
            f.seek(0)

            return f.read()
    else:
        raise Exception(f'File at "{path}" does not exist')

def retrieve_download_text_files(path: str):
    (_, _, files) = os.walk(path).__next__()
    print(files)

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

    while i < len(x):
        if to_search == x[i:i + len(to_search)]:
            return True
        
        i += 1
    return False

def count_sub_str(x: str, to_search: str):
    i, j = 0, 0

    while j < len(x):
        if to_search == x[j:j + len(to_search)]:
            i += 1
        j += 1
    return i