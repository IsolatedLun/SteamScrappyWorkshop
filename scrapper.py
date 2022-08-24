from includes.Log4Py.log4Py import Logger
from consts import STEAM_APP_URL, STEAM_URL

import requests
import __main__

logger = Logger(__main__)

logger.set_level('special', 34)


def scrape_collection(appId: int, collectionId: int):
    """
        Scrapes the items id's of a steam collection.
    """

    def getCollectionTitle(soup):
        return soup.select('.workshopItemTitle')[0].text

    from bs4 import BeautifulSoup as bs

    app_name = is_valid_app_id(appId)
    collection_name = ''
    if not app_name:
        logger.error(f'{appId} is not a valid application ID')
        return
    else:
        logger.special(f'> Detected app: {app_name}')

    logger.log(f'> Opening {STEAM_URL + str(collectionId)}')

    req = requests.get(STEAM_URL + str(collectionId))
    soup = bs(req.text, 'lxml')

    collection_name = getCollectionTitle(soup)
    text = soup.select('.rightSectionTopTitle')[0]

    logger.special(f'> Detected collection: {collection_name}')

    i = 0
    out = 'steamcmd +login anonymous'
    if text.text.find('collection') > -1:
        a_tags = soup.select('.collectionItem')

        for item in a_tags:
            x = item['id'].split('_')[1]
            out += ' +' + f'workshop_download_item {appId} {x}'
            i += 1

            logger.log(f'> Found item: {x}')

    with open(f'{app_name}-{collection_name}.txt', 'w') as f:
        f.write(out)

    return i, out

# ===============
# Utils
# ==============


def is_valid_app_id(appId: int):
    from bs4 import BeautifulSoup as bs

    res = requests.get(STEAM_APP_URL + str(appId)).text
    data = bs(res, 'lxml').select('.apphub_AppName')

    if len(data) > 0:
        return data[0].text
    return False


def sanitize_steamcmd_command(command: str):
    return command
