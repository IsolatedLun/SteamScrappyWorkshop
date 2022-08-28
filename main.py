import __main__
import os
from shlex import split as shlex_split
from src.consts import BASE_DIR, STEAMCMD_WORKSHOP, VERSION
from src.handlers.alias_handler import show_alias
from src.utils import (clean_quotes, get_arg_index, output_commands,
                       read_output_file, show_items, show_welcome, show_help)

from includes.Log4Py.log4Py import Logger
from src.scrapper import scrape_root

if __name__ == '__main__':
    data = {}
    loop = True
    opened_steamcmd = False
    logger = Logger(__main__)

    show_welcome(VERSION)  # No need to log useless info
    while loop:
        try:
            _input = input('>| ').strip()

            # ======================
            # Downloading commands
            # ======================
            if _input.startswith('collection'):
                alias, collectionId, *options = tuple(shlex_split(_input)[1:])

                item_count, items = scrape_root(
                    'collection', clean_quotes(alias), collectionId)
                logger.alter(f'> Found {item_count} item(s)')

                data = data | items

            elif _input.startswith('search'):
                alias, query, *options = tuple(shlex_split(_input)[1:])
                items = scrape_root('search', clean_quotes(
                    alias), clean_quotes(query))

                data = data | items

            elif _input.startswith('download'):
                file_name, *options = tuple(shlex_split(_input)[1:])

                path_dir = os.path.join(BASE_DIR, file_name)
                opened_steamcmd = True

                read_output_file(path_dir)

            # ======================
            # Outputting commands
            # ======================
            elif _input.startswith('output'):
                options = shlex_split(_input)[1:]
                out = ''
                i = 0

                for item in data.keys():
                    (app_id, name, id, *_) = data[item].values()
                    out += STEAMCMD_WORKSHOP.format(app_id, id)

                    i += 1

                dir = output_commands(out, options, 'items', i)
                logger.alter(f'> Created output file at: {dir} with {i} items')

            # ======================
            # Altering/Editing commands
            # ======================
            elif _input.startswith('items'):
                options = shlex_split(_input)[1:]

                if '--remove' in options:
                    idx = get_arg_index(options, '--remove')
                    val = int(options[idx])

                    if data.get(val, False):
                        del data[val]
                        logger.alter(f'Removed item: {val}')
                    else:
                        logger.error(
                            f'Item with an index of "{val}" not found')
                    continue

                res, item_count = show_items(data)

                if item_count > 0:
                    logger.log('\n' + res)
                logger.alter(f'> Found {item_count} item(s)')

            # ======================
            # Printing commands
            # ======================
            elif _input == 'help':
                show_help()
            elif _input == 'aliases':
                i = show_alias()

                logger.alter(f'> Found {i} aliases(s)')

            # ======================
            # Misc commands
            # ======================
            elif _input.startswith('exit'):
                loop = False
            else:
                logger.warn(
                    f'> Command not found: "{_input}", type help for options')

            opened_steamcmd = False
        except Exception as e:
            logger.error(f'> {e}')

    logger.warn('Exitting...')
