# =========================
# Printing functions
# =========================
import os

from src.consts import BASE_DIR, STEAMCMD_LOGIN, load_config


def show_all_commands(v: int):
    # TODO: Create a command dict that stores the command and it's details to automate it.
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
collection  <app id or name> <collection id> --download(Automatically download items with steamcmd)
search      <app id or name> <query> --download(Automatically download items with steamcmd)

aliases     Shows all aliases.
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

    out_dir = os.path.join(BASE_DIR, out_dir)
    with open(out_dir, config['mode']) as f:
        f.seek(0)  # goto the 1st line

        data = f.readline()

        if data.startswith('steamcmd'):
            f.write(out)
        else:
            f.write(STEAMCMD_LOGIN + out)

# =========================
# Command functions
# =========================


def get_arg_index(commands: list[str], command):
    return commands.index(command) + 1
