# =========================
# Printing functions
# =========================
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
exit        Exits the app.
------------------------------------
"""

# =========================
# Command functions
# =========================


def get_arg_index(commands: list[str], command):
    return commands.index(command) + 1


def create_steamcmd_command():
    """
        Returns the default anonymous login command
    """
    return 'steamcmd +login anonymous'
