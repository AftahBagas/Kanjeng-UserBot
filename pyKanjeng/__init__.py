import time

import heroku3

from .Config import Config
from .core import logger
from .core.session import kanjeng

__version__ = "3.0.0"
__license__ = "GNU Affero General Public License v3.0"
__author__ = "KanjengBot <https://github.com/AftahBagas/Kanjeng-Userbot>"
__copyright__ = "KanjengBot Copyright (C) 2020 - 2021  " + __author__

kanjeng.version = __version__
kanjeng.tgbot.version = __version__
bot = kanjeng

StartTime = time.time()
kanjengversion = "3.0.0"

if Config.UPSTREAM_REPO == "Kanjeng-Userbot":
    UPSTREAM_REPO_URL = "https://github.com/AftahBagas/Kanjeng-Userbot"
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
