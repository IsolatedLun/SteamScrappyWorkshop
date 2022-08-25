# =========================
# Printing functions
# =========================
import json

from consts import STEAMCMD_LOGIN


def show_all_commands(v: int):
    return \
        f"""
SteamScrappyDownloader v{v}
______________________
{show_help()}
"""


def show_help():
    return \
        """
COMMANDS:
------------------------------------
collection  <app_id> <collection_id> --download(Automatically download items with steamcmd)
search      <app_id> <query> --download(Automatically download items with steamcmd)
exit        Exits the app.
------------------------------------
"""

# =========================
# Writing functions
# =========================


def output_commands(out: str, *vars: list[str]):
    config = load_config()

    out_dir = ''
    if config['out_dir']:
        out_dir = config['out_dir']
    else:
        out_dir = '-'.join(vars)

    with open(out_dir, config['mode']) as f:
        f.seek(0)  # goto the 1st line

        data = f.readline()

        if data.startswith('steamcmd'):
            print('No login')
            f.write(out)
        else:
            print('Added login')
            f.write(STEAMCMD_LOGIN + out)


def load_config():
    with open('config.json', 'r') as f:
        return json.loads(f.read())

# =========================
# Command functions
# =========================


def get_arg_index(commands: list[str], command):
    return commands.index(command) + 1
