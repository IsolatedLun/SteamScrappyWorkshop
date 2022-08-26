from ast import alias
import json
import os

from src.consts import ALIASES_DIR


def handle_alias(app_alias: str):
    def sanitize_text(text: str):
        return '-'.join([x for x in text.split(' ')]).lower()

    def set(name: str):
        if app_alias.isnumeric():
            with open(ALIASES_DIR, 'r+') as f:
                aliases[sanitize_text(name)] = app_alias
                json.dump(aliases, f)

    with open(ALIASES_DIR, 'r+') as f:
        aliases = json.load(f)
        is_in_aliases = True if aliases.get(
            app_alias.lower(), False) else False

        return aliases.get(sanitize_text(app_alias), app_alias), is_in_aliases, set


def show_alias():
    with open(ALIASES_DIR, 'r') as f:
        aliases = json.load(f)
        i = 0

        for (name, id) in aliases.items():
            print('-' * 48)
            print(f'| {name} -> {id}')
            i += 1

        print('-' * 48)
        print(f'> Found {i} aliases')
