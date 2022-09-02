import os
from src.handlers.alias_handler import handle_alias
from src.utils import get_arg_index, output_commands, sanitize_text
from includes.Log4Py.log4Py import Logger
from src.consts import STEAM_APP_URL, STEAM_SEARCH_URL, STEAM_URL, STEAMCMD_DIR, STEAMCMD_WORKSHOP

import requests
import __main__

logger = Logger(__main__)
logger.set_level('special', 34)


def scrape_root(scrape_type: str, alias: int, options: list[str], data_len, *args):
    """
        Validates the app id then calls the scraper with it's arguments depeding on the type
    """
    app_name, app_id = is_valid_app_id(alias)
    logger.special(f'> Detected app: {app_name}')

    if scrape_type == 'collection':
        return scrape_collection(app_name, app_id, options, data_len, *args)
    elif scrape_type == 'search':
        return scrape_search(app_name, app_id, options, data_len, *args)
    else:
        logger.error(f'Scrapper "{scrape_type}" not found')


def scrape_collection(app_name: str, app_id: str, collection_id: str, options: list[str], data_len):
    """
        Scrapes the items id's of a steam collection.
    """
    from bs4 import BeautifulSoup as bs

    def getCollectionTitle(soup):
        """
            Gets the name of the title
        """
        return soup.select('.workshopItemTitle')[0].text

    # Assertion 1
    if not collection_id.isnumeric():
        logger.error(f"> Collection id must only contain numbers")
        return 0, 0

    logger.log(f'> Opening {STEAM_URL + str(collection_id)}')

    req = requests.get(STEAM_URL + str(collection_id))
    req_title = bs(req.text, 'html.parser').title.text

    # Assertion 2
    if req_title.endswith('Error'):
        logger.error(f"> Invalid collection '{collection_id}'")
        return 0, 0

    soup = bs(req.text, 'lxml')

    collection_name = getCollectionTitle(soup)
    text = soup.select('.rightSectionTopTitle')[0]

    logger.special(f'> Detected collection: {collection_name}')

    i = 0
    out = {}
    if text.text.find('collection') > -1:
        a_tags = soup.select('.collectionItem')

        for item in a_tags:
            item_id = item['id'].split('_')[1]
            item_name = item.select('.workshopItemTitle')[0].text

            out[item_id] = {'app_id': app_id,
                            'name': item_name, 'id': item_id}
            i += 1

            logger.log(f'> Found: {item_name}')

    return i, out


def scrape_search(app_name: str, app_id: int, options: list[str], data_len, query: str):
    """
        Scrapes an app's search page for items depeding on the query.
    """
    from bs4 import BeautifulSoup as bs

    def getItemDetails(item):
        """
            Gets the item name and id
        """
        item_name = item.select('.workshopItemTitle')[0].text
        item_id = item.select(
            '.ugc[data-publishedfileid]')[0]['data-publishedfileid']

        return item_name, item_id

    page = 1
    if '--page' in options:
        idx = get_arg_index(options, '--page')
        page = options[idx]

    logger.log(f'> Opening {STEAM_SEARCH_URL.format(app_id, query, page)}')

    req = requests.get(STEAM_SEARCH_URL.format(app_id, query, page))
    soup = bs(req.text, 'lxml')

    i = 1
    out = {}
    cache = {}
    for item in soup.select('.workshopItem'):
        item_name, item_id = getItemDetails(item)
        # Storing by index for simplicity
        cache[i] = {'id': item_id, 'name': item_name}

        logger.log(f'> {i}) {item_name} - {item_id}')
        i += 1

    selected = input('>> Select items [all/indexes/exit]: ')

    if selected == 'all':
        logger.special('Adding all items...')
        for i, (idx, item) in enumerate(cache.items()):
            out[data_len + i] = {'app_id': app_id,
                                 'name': item['name'], 'id': item['id']}

            logger.special(f'> Adding item: ' + item['name'])
    elif selected[0].isnumeric():
        for i, idx in enumerate(selected.split(' ')):
            # Converting idx to int because it str and int hashes are different.
            if cache.get(int(idx), False):
                (_, id), (_, name) = cache[int(idx)].items()
                out[data_len + i] = {'app_id': app_id, 'name': name, 'id': id}

                logger.special(f'> Adding item: {name}')
            else:
                logger.error(f'> {idx} not found')

    return out

# ===============
# Utils
# ==============


def is_valid_app_id(alias: str):
    from bs4 import BeautifulSoup as bs

    app_id, is_in_aliases, set_alias = handle_alias(alias)

    res = requests.get(STEAM_APP_URL + str(app_id)).text
    data = bs(res, 'lxml').select('.apphub_AppName')

    if len(data) > 0:
        text = data[0].text

        if not is_in_aliases:
            set_alias(text)
            logger.special(f'Added alias {text} => {app_id}')

        return text, app_id
    raise Exception(f'"{app_id}" is not a valid application ID')


def sanitize_steamcmd_command(command: str):
    """
        Sanitizes the command that will be ran by the os.
    """
    if command.startswith('steamcmd'):
        return command
    else:
        return 'steamcmd' + command


def run_steamcmd(command):
    os.system(f'cd {STEAMCMD_DIR} && {sanitize_steamcmd_command(command)}')
