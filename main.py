import __main__
from src.consts import STEAMCMD_WORKSHOP, VERSION
from src.handlers.alias_handler import show_alias
from src.utils import output_commands, show_items, show_welcome, show_help

from includes.Log4Py.log4Py import Logger
from src.scrapper import scrape_root

if __name__ == '__main__':
    data = {}
    loop = True
    logger = Logger(__main__)

    show_welcome(VERSION)  # No need to log useless info
    while loop:
        _input = input('>| ')

        # ======================
        # Downloading commands
        # ======================
        if _input.startswith('collection'):
            alias, collectionId, *options = tuple(_input.split(' ')[1:])

            item_count, items = scrape_root(
                'collection', alias, collectionId)
            logger.alter(f'> Found {item_count} item(s)')

            data = data | items

        elif _input.startswith('search'):
            alias, query, *options = tuple(_input.split(' ')[1:])
            items = scrape_root('search', alias, query)

            data = data | items

        # ======================
        # Outputting commands
        # ======================
        elif _input == 'output':
            out = ''
            i = 0

            for item in data.keys():
                (app_id, name, id, *_) = data[item].values()
                out += STEAMCMD_WORKSHOP.format(app_id, id)

                i += 1

            output_commands(out, 'items', i)

        # ======================
        # Printing commands
        # ======================
        elif _input == 'help':
            show_help()
        elif _input == 'aliases':
            show_alias()
        elif _input == 'items':
            res, item_count = show_items(data)

            logger.log(res)
            logger.alter(f'> Found {item_count} item(s)')

        elif _input.startswith('exit'):
            loop = False
        else:
            logger.warn(
                f'> Command not found: "{_input}", type help for options')
    logger.warn('Exitting...')
