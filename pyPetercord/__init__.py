import time

import heroku3

from .Config import Config
from .core import logger
from .core.session import petercord

__version__ = "3.0.0"
__license__ = "GNU Affero General Public License v3.0"
__author__ = "PetercordBot <https://github.com/IlhamMansiez/PetercordBot>"
__copyright__ = "PetercordBot Copyright (C) 2020 - 2021  " + __author__

petercord.version = __version__
petercord.tgbot.version = __version__
bot = petercord

StartTime = time.time()
catversion = "3.0.0"

if Config.UPSTREAM_REPO == "petercord":
    UPSTREAM_REPO_URL = "https://github.com/IlhamMansiez/PetercordBot"
else:
    UPSTREAM_REPO_URL = Config.UPSTREAM_REPO

if Config.PRIVATE_GROUP_BOT_API_ID == 0:
    BOTLOG = False
    BOTLOG_CHATID = "me"
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID

try:
    if Config.HEROKU_API_KEY is not None or Config.HEROKU_APP_NAME is not None:
        HEROKU_APP = heroku3.from_key(Config.HEROKU_API_KEY).apps()[
            Config.HEROKU_APP_NAME
        ]
    else:
        HEROKU_APP = None
except Exception:
    HEROKU_APP = None


# Global Configiables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
ISAFK = False
AFKREASON = None
CMD_LIST = {}
SUDO_LIST = {}
# for later purposes
INT_PLUG = ""
LOAD_PLUG = {}
