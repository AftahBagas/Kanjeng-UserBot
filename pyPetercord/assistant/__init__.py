from pyPetercord import petercord

from ..Config import Config
from ..core.inlinebot import *

if Config.PRIVATE_GROUP_BOT_API_ID == 0:
    BOTLOG = False
    BOTLOG_CHATID = "me"
else:
    BOTLOG = True
    BOTLOG_CHATID = Config.PRIVATE_GROUP_BOT_API_ID
