from includes.Log4Py.log4Py import Logger
from consts import STEAM_APP_URL, STEAM_URL

import requests
import __main__

logger = Logger(__main__)

logger.set_level('special', 34)


def scrape_collection(appId: int, collectionId: int):
    from bs4 import BeautifulSoup as bs

    app_name = is_valid_app_id(appId)
    if not app_name:
        logger.error(f'{appId} is not a valid application ID')
        return
    else:
        logger.special(f'> Detected app: {app_name}')

    logger.log(f'> Opening {STEAM_URL + str(collectionId)}')

    req = requests.get(STEAM_URL + str(collectionId))
    soup = bs(req.text, 'lxml')

    text = soup.select('.rightSectionTopTitle')[0]

    i = 0
    out = 'steamcmd +login anonymous'
    if text.text.find('collection') > -1:
        a_tags = soup.select('.collectionItem')

        for item in a_tags:
            x = item['id'].split('_')[1]
            out += ' +' + f'workshop_download_item {appId} {x}'
            i += 1

            logger.log(f'> Found item: {x}')

    with open('out.txt', 'w') as f:
        f.write(out)

    return i

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
