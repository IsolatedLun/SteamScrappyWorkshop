from helper import create_steamcmd_command
from includes.Log4Py.log4Py import Logger
from consts import STEAM_APP_URL, STEAM_SEARCH_URL, STEAM_URL, STEAMCMD_WORKSHOP

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
    out = create_steamcmd_command()  # Login command
    if text.text.find('collection') > -1:
        a_tags = soup.select('.collectionItem')

        for item in a_tags:
            x = item['id'].split('_')[1]
            # Download command
            out += STEAMCMD_WORKSHOP.format(appId, id)
            i += 1

            logger.log(f'> Found item: {x}')

    with open(f'{app_name}-{collection_name}.txt', 'w') as f:
        f.write(out)

    logger.alter('> DONE')

    return i, out


def scrape_search(appId: int, query: str):
    """
        Scrapes an app's search page for items depeding on the query.
    """

    def get_item_details(item):
        item_name = item.select('.workshopItemTitle')[0].text
        item_id = item.select(
            '.ugc[data-publishedfileid]')[0]['data-publishedfileid']

        return item_name, item_id

    from bs4 import BeautifulSoup as bs

    app_name = is_valid_app_id(appId)
    if not app_name:
        logger.error(f'{appId} is not a valid application ID')
        return
    else:
        logger.special(f'> Detected app: {app_name}')

    logger.log(f'> Opening {STEAM_SEARCH_URL.format(appId, query)}')

    req = requests.get(STEAM_SEARCH_URL.format(appId, query))
    soup = bs(req.text, 'lxml')

    i = 1
    out = create_steamcmd_command()
    cache = {}
    for item in soup.select('.workshopItem'):
        item_name, item_id = get_item_details(item)
        # Storing by index for simplicity
        cache[i] = {'id': item_id, 'name': item_name}

        logger.log(f'> {i}) {item_name} - {item_id}')
        i += 1

    selected = input('>> Select items [all/indexes]: ')

    if selected == 'all':
        logger.special('Adding all items...')
        for (id, item) in cache.items():
            out += STEAMCMD_WORKSHOP.format(appId, item['id'])
            logger.special(f'> Adding item: ' + item['name'])
    else:
        for idx in selected.split(' '):
            # Converting idx to int because it str and int hashes are different.
            (_, id), (_, name) = cache[int(idx)].items()
            out += STEAMCMD_WORKSHOP.format(appId, id)

            logger.special(f'> Adding item: {name}')

    with open(f'{app_name}-search-{query}.txt', 'w') as f:
        f.write(out)

    return out

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
    """
        Sanitizes the command that will be ran by the os.
    """
    if command.startswith('steamcmd'):
        return command
    else:
        return 'steamcmd' + command
