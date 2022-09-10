import json

from src.consts import ALIASES_DIR, DASH_LENGTH, load_aliases
from src.utils import sanitize_text

def handle_alias(app_alias: str):
    def set(name: str):
        if app_alias.isnumeric():
            with open(ALIASES_DIR, 'r+') as f:
                aliases[sanitize_text(name)] = app_alias
                json.dump(aliases, f)

    aliases = load_aliases()
    is_in_aliases = True if aliases.get(
        app_alias.lower(), False) else False

    return aliases.get(sanitize_text(app_alias), app_alias), is_in_aliases, set

def get_alias_by_app_id(app_id: str):
    reversed_aliases = {v:k for (k, v) in load_aliases().items()}

    return reversed_aliases.get(app_id, app_id)

def show_alias():
    aliases = load_aliases()
    i = 0

    print('\n' + '-' * DASH_LENGTH)
    for (name, id) in aliases.items():
        print(f'| {name} -> {id}')
        print('-' * DASH_LENGTH)

        i += 1

    return i
