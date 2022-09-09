import os

from src.consts import BASE_DIR, OUTPUT_IDENTIFIER, BLACKLISTED_DIRS
from src.utils import sub_str

def get_scrappyd_files():
    files_dict = {}
    for root, dirs, files in os.walk(BASE_DIR, topdown=True):
        if dirs in BLACKLISTED_DIRS:
            break

        for file in files:
            if sub_str(file, f'[{OUTPUT_IDENTIFIER}].txt'):
                files_dict[file] = f'{root}/{file}'

    return files_dict

def get_scrappyd_files_by_index(idx: int):
    files = get_scrappyd_files()

    if idx > len(files) - 1:
        raise Exception(f'> The file with an index of "{idx}" does not exist') 

    for i, (name, path) in enumerate(files.items()):
        if i == idx:
            return path

def show_files():
    files = get_scrappyd_files()

    print('-' * 48)
    for i, (name, path) in enumerate(files.items()):
        print(f'| {name} -> [{i}]')
        print('-' * 48)
