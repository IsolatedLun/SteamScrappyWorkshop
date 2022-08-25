import os
import __main__
from consts import VERSION
from helper import show_all_commands, show_help

from includes.Log4Py.log4Py import Logger
from scrapper import sanitize_steamcmd_command, scrape_collection, scrape_search

if __name__ == '__main__':
    loop = True
    STEAMCMD_DIR = 'C:/Users/user/Desktop/steamcmd'

    logger = Logger(__main__)

    print(show_all_commands(VERSION))
    while loop:
        _input = input('>| ')

        if _input.startswith('collection'):
            appId, collectionId, *options = tuple(_input.split(' ')[1:])

            item_count, command = scrape_collection(appId, collectionId)
            logger.alter(f'> Found {item_count} item(s)')

            if '--download' in options:
                logger.alter(f'> Opening steamcmd client')
                os.system(
                    f'cd {STEAMCMD_DIR} && {sanitize_steamcmd_command(command)}')

        elif _input.startswith('search'):
            appId, query, *options = tuple(_input.split(' ')[1:])
            command = scrape_search(appId, query)

            if '--download' in options:
                logger.alter(f'> Opening steamcmd client')
                os.system(
                    f'cd {STEAMCMD_DIR} && {sanitize_steamcmd_command(command)}')

        elif _input.startswith('search'):
            appId, *options = tuple(_input.split(' ')[1:])

        elif _input == 'help':
            print(show_help())

        elif _input == 'exit':
            loop = False
        else:
            logger.warn(
                f'> Command not found: "{_input}", type help for options')
    logger.warn('Exitting...')
