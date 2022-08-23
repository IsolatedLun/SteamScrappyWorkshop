from consts import STEAM_URL
import __main__


from bs4 import BeautifulSoup
from includes.Log4Py.log4Py import Logger
from scrapper import scrape_collection

if __name__ == '__main__':
    loop = True
    STEAMCMD_DIR = 'C:/Users/user/Desktop/steamcmd'

    logger = Logger(__main__)

    while loop:
        _input = input('>| ')

        if _input.startswith('collection'):
            appId, collectionId, *options = tuple(_input.split(' ')[1:])

            item_count = scrape_collection(appId, collectionId)
            logger.alter(f'> Found {item_count} item(s)')

        if _input == 'exit':
            loop = False
    logger.warn('Exitting...')
