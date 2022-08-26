import __main__
from src.consts import VERSION
from src.handlers.alias_handler import show_alias
from src.utils import show_all_commands, show_help

from includes.Log4Py.log4Py import Logger
from src.scrapper import scrape_root, run_steamcmd

if __name__ == '__main__':
    loop = True
    logger = Logger(__main__)

    print(show_all_commands(VERSION))  # No need to log useless info
    while loop:
        _input = input('>| ')

        if _input.startswith('collection'):
            alias, collectionId, *options = tuple(_input.split(' ')[1:])

            item_count, command = scrape_root(
                'collection', alias, collectionId)
            logger.alter(f'> Found {item_count} item(s)')

            if '--download' in options:
                logger.alter(f'> Opening steamcmd client')
                run_steamcmd(command)

        elif _input.startswith('search'):
            appId, query, *options = tuple(_input.split(' ')[1:])
            command = scrape_root('search', appId, query)

            if '--download' in options:
                logger.alter(f'> Opening steamcmd client')
                run_steamcmd(command)

        elif _input == 'help':
            print(show_help())
        elif _input == 'aliases':
            show_alias()

        elif _input == 'exit':
            loop = False
        else:
            logger.warn(
                f'> Command not found: "{_input}", type help for options')
    logger.warn('Exitting...')
