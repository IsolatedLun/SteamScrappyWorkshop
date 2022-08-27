import os
from src.handlers.alias_handler import handle_alias
from src.utils import output_commands, sanitize_text
from includes.Log4Py.log4Py import Logger
from src.consts import STEAM_APP_URL, STEAM_SEARCH_URL, STEAM_URL, STEAMCMD_DIR, STEAMCMD_WORKSHOP

import requests
import __main__

logger = Logger(__main__)
logger.set_level('special', 34)


def scrape_root(scrape_type: str, alias: int,  *args):
    """
        Validates the app id then calls the scraper with it's arguments depeding on the type
    """
    app_name, app_id = is_valid_app_id(alias)

    if not app_name:
        logger.error(f'{app_id} is not a valid application ID')
        return
    else:
        logger.special(f'> Detected app: {app_name}')

    if scrape_type == 'collection':
        return scrape_collection(app_name, app_id, *args)
    elif scrape_type == 'search':
        return scrape_search(app_name, app_id, *args)
    else:
        logger.error(f'Scrapper "{scrape_type}" not found')


def scrape_collection(app_name: str, app_id: str, collectionId: str):
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
    if not collectionId.isnumeric():
        logger.error(f"> Collection id must only contain numbers")
        return 0, 0

    logger.log(f'> Opening {STEAM_URL + str(collectionId)}')

    req = requests.get(STEAM_URL + str(collectionId))
    req_title = bs(req.text, 'html.parser').title.text

    # Assertion 2
    if req_title.endswith('Error'):
        logger.error(f"> Invalid collection '{collectionId}'")
        return 0, 0

    soup = bs(req.text, 'lxml')

    collection_name = getCollectionTitle(soup)
    text = soup.select('.rightSectionTopTitle')[0]

    logger.special(f'> Detected collection: {collection_name}')

    i = 0
    out = ''
    if text.text.find('collection') > -1:
        a_tags = soup.select('.collectionItem')

        for item in a_tags:
            x = item['id'].split('_')[1]
            # Download command
            out += STEAMCMD_WORKSHOP.format(app_id, id)
            i += 1

            logger.log(f'> Found item: {x}')

    with open(f'{app_name}-{collection_name}.txt', 'w') as f:
        f.write(out)

    logger.alter('> DONE')
    output_commands(out, app_name, collection_name)

    return i, out


def scrape_search(app_name: str, app_id: int, query: str):
    """
        Scrapes an app's search page for items depeding on the query.
    """
    from bs4 import BeautifulSoup as bs

    def get_item_details(item):
        """
            Gets the item name and id
        """
        item_name = item.select('.workshopItemTitle')[0].text
        item_id = item.select(
            '.ugc[data-publishedfileid]')[0]['data-publishedfileid']

        return item_name, item_id

    logger.log(f'> Opening {STEAM_SEARCH_URL.format(app_id, query)}')

    req = requests.get(STEAM_SEARCH_URL.format(app_id, query))
    soup = bs(req.text, 'lxml')

    i = 1
    out = {}
    cache = {}
    for item in soup.select('.workshopItem'):
        item_name, item_id = get_item_details(item)
        # Storing by index for simplicity
        cache[i] = {'id': item_id, 'name': item_name}

        logger.log(f'> {i}) {item_name} - {item_id}')
        i += 1

    selected = input('>> Select items [all/indexes/exit]: ')

    if selected == 'all':
        logger.special('Adding all items...')
        for (idx, item) in cache.items():
            sanitized_name = sanitize_text(item['name'])
            out[sanitized_name] = {'app_id': app_id,
                                   'name': item['name'], 'id': item['id'], 'index': idx}

            logger.special(f'> Adding item: ' + item['name'])
    elif selected[0].isnumeric():
        for idx in selected.split(' '):
            try:
                # Converting idx to int because it str and int hashes are different.
                (_, id), (_, name) = cache[int(idx)].items()
                sanitized_name = sanitize_text(name)
                out[sanitized_name] = {'app_id': app_id,
                                       'name': name, 'id': id, 'index': idx}

                logger.special(f'> Adding item: {name}')
            except:
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
            logger.special(f'Added alias {text} - {app_id}')

        return text, app_id
    return False, -1


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
