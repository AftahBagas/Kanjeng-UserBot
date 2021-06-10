import glob
import os
import sys
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils

import pyKanjeng
from pyKanjeng import BOTLOG, BOTLOG_CHATID

from .Config import Config
from .core.logger import logging
from .core.session import kanjeng
from .helpers.utils import install_pip
from .sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from .sql_helper.globals import gvarstatus
from .utils import load_module

LOGS = logging.getLogger("KanjengBot")

print(pyKanjeng.__copyright__)
print("Licensed under the terms of the " + pyKanjeng.__license__)

cmdhr = Config.COMMAND_HAND_LER


async def testing_bot():
    try:
        await kanjeng.connect()
        config = await petercord(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == kanjeng.session.server_address:
                if kanjeng.session.dc_id != option.id:
                    LOGS.warning(
                        f"Fixed DC ID in session from {petercord.session.dc_id}"
                        f" to {option.id}"
                    )
                kanjeng.session.set_dc(option.id, option.ip_address, option.port)
                kanjeng.session.save()
                break
        await kanjeng.start(bot_token=Config.TG_BOT_USERNAME)
        kanjeng.me = await kanjeng.get_me()
        kanjeng.uid = kanjeng.tgbot.uid = utils.get_peer_id(kanjeng.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(kanjeng.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {str(e)}")
        sys.exit()


def verifyLoggerGroup():
    if BOTLOG:
        try:
            entity = kanjeng.loop.run_until_complete(
                petercord.get_entity(BOTLOG_CHATID)
            )
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified Logger group."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified Logger group."
                    )
        except ValueError:
            LOGS.error("Logger group ID cannot be found. " "Make sure it's correct.")
        except TypeError:
            LOGS.error("Logger group ID is unsupported. " "Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the logger group.\n"
                + str(e)
            )
        try:
            entity = kanjeng.loop.run_until_complete(
                kanjeng.get_entity(Config.PM_LOGGER_GROUP_ID)
            )
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "Permissions missing to send messages for the specified Pm logger group."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "Permissions missing to addusers for the specified Pm Logger group."
                    )
        except ValueError:
            LOGS.error("Pm Logger group ID cannot be found. " "Make sure it's correct.")
        except TypeError:
            LOGS.error("Pm Logger group ID is unsupported. " "Make sure it's correct.")
        except Exception as e:
            LOGS.error(
                "An Exception occured upon trying to verify the Pm logger group.\n"
                + str(e)
            )
    else:
        LOGS.info(
            "You haven't set the PRIVATE_GROUP_BOT_API_ID in vars please set it for proper functioning of userbot."
        )


def add_bot_to_logger_group():
    bot_details = kanjeng.loop.run_until_complete(kanjeng.tgbot.get_me())
    Config.TG_BOT_USERNAME = f"@{bot_details.username}"
    try:
        kanjeng.loop.run_until_complete(
            kanjeng(
                functions.messages.AddChatUserRequest(
                    chat_id=BOTLOG_CHATID,
                    user_id=bot_details.username,
                    fwd_limit=1000000,
                )
            )
        )
        kanjeng.loop.run_until_complete(
            catub(
                functions.messages.AddChatUserRequest(
                    chat_id=Config.PM_LOGGER_GROUP_ID,
                    user_id=bot_details.username,
                    fwd_limit=1000000,
                )
            )
        )
    except BaseException:
        try:
            kanjeng.loop.run_until_complete(
                kanjeng(
                    functions.channels.InviteToChannelRequest(
                        channel=BOTLOG_CHATID,
                        users=[bot_details.username],
                    )
                )
            )
            kanjeng.loop.run_until_complete(
                petercord(
                    functions.channels.InviteToChannelRequest(
                        channel=Config.PM_LOGGER_GROUP_ID,
                        users=[bot_details.username],
                    )
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def startupmessage():
    try:
        if BOTLOG:
            Config.KANJENGLOGO = await kanjeng.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/95c9129cdf77386baf440.jpg",
                caption="**Your Kanjeng Userbot has been started successfully.**",
                buttons=[
                    (Button.url("Support", "https://t.me/TeamSquadUserbotSupport"),)
                ],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await kanjeng.check_testcases()
            message = await kanjeng.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n**Ok Bot is Back and Alive.**"
            await kanjeng.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await kanjeng.send_message(
                    msg_details[0],
                    f"{cmdhr}ping",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


if len(sys.argv) not in (1, 3, 4):
    kanjeng.disconnect()
else:
    try:
        LOGS.info("Starting Kanjeng Userbot")
        kanjeng.loop.run_until_complete(testing_bot())
        LOGS.info("Startup Completed")
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()

verifyLoggerGroup()
add_bot_to_logger_group()

path = "pyKanjeng/plugins/*.py"
files = glob.glob(path)
files.sort()
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        try:
            if shortname.replace(".py", "") not in Config.NO_LOAD:
                flag = True
                check = 0
                while flag:
                    try:
                        load_module(shortname.replace(".py", ""))
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if check > 5:
                            break
            else:
                os.remove(Path(f"pyKanjeng/plugins/{shortname}.py"))
        except Exception as e:
            os.remove(Path(f"pyKanjeng/plugins/{shortname}.py"))
            LOGS.info(f"unable to load {shortname} because of error {e}")

path = "pyKanjeng/assistant/*.py"
files = glob.glob(path)
files.sort()
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        try:
            if shortname.replace(".py", "") not in Config.NO_LOAD:
                flag = True
                check = 0
                while flag:
                    try:
                        load_module(
                            shortname.replace(".py", ""),
                            plugin_path="pyKanjeng/assistant",
                        )
                        break
                    except ModuleNotFoundError as e:
                        install_pip(e.name)
                        check += 1
                        if check > 5:
                            break

            else:
                os.remove(Path(f"pyKanjeng/assistant/{shortname}.py"))
        except Exception as e:
            os.remove(Path(f"pyKanjeng/assistant/{shortname}.py"))
            LOGS.info(f"unable to load {shortname} because of error {e}")
            LOGS.info(f"{e.args}")

print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")
print("Yay your userbot is officially working.!!!")
print(
    f"Congratulation, now type {cmdhr}alive to see message if Kanjeng Userbot is live\
      \nTelah aktif Join grup https://t.me/TeamSquadUserbotSupport"
)
print("➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖")

verifyLoggerGroup()
add_bot_to_logger_group()
kanjeng.loop.create_task(startupmessage())

if len(sys.argv) not in (1, 3, 4):
    kanjeng.disconnect()
else:
    kanjeng.run_until_disconnected()
