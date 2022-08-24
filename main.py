import os
import __main__
from consts import VERSION
from helper import show_all_commands, show_help

from includes.Log4Py.log4Py import Logger
from scrapper import scrape_collection

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
                os.system(f'cd {STEAMCMD_DIR} && {command}')
        elif _input == 'help':
            print(show_help())

        if _input == 'exit':
            loop = False
    logger.warn('Exitting...')
