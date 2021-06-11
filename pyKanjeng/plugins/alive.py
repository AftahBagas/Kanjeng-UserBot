import re
import time
from platform import python_version

from telethon import version
from telethon.events import CallbackQuery

from pyKanjeng import StartTime, kanjeng, kanjengversion

from ..Config import Config
from ..core.managers import edit_or_reply
from ..helpers.functions import (
    check_data_base_heal_th,
    get_readable_time,
    petercordalive,
)
from ..helpers.utils import reply_id
from . import mention

CUSTOM_ALIVE_TEXT = (
    Config.CUSTOM_ALIVE_TEXT or "✮ KANJENG USERBOT IS RUNNING SUCCESSFULLY ✮"
)
EMOJI = Config.CUSTOM_ALIVE_EMOJI or " 🔸 "

plugin_category = "utils"


@kanjeng.alfareza_cmd(
    pattern="alive$",
    command=("alive", plugin_category),
    info={
        "header": "To check bot's alive status",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details"
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    _, check_sgnirts = check_data_base_heal_th()
    if Config.ALIVE_PIC:
        kanjeng_caption = f"**{CUSTOM_ALIVE_TEXT}**\n\n"
        kanjeng_caption += f"**{EMOJI} Database :** `{check_sgnirts}`\n"
        kanjeng_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
        kanjeng_caption += f"**{EMOJI} Kanjeng Version :** `{kanjengversion}`\n"
        kanjeng_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
        kanjeng_caption += f"**{EMOJI} Uptime :** `{uptime}\n`"
        kanjeng_caption += f"**{EMOJI} Kanjeng:** {mention}\n"
        await event.client.send_file(
            event.chat_id,
            Config.ALIVE_PIC,
            caption=petercord_caption,
            reply_to=reply_to_id,
        )
        await event.delete()
    else:
        await edit_or_reply(
            event,
            f"**{CUSTOM_ALIVE_TEXT}**\n\n"
            f"**{EMOJI} Database :** `{check_sgnirts}`\n"
            f"**{EMOJI} Telethon Version :** `{version.__version__}\n`"
            f"**{EMOJI} Kanjeng Version :** `{kanjengversion}`\n"
            f"**{EMOJI} Python Version :** `{python_version()}\n`"
            f"**{EMOJI} Uptime :** `{uptime}\n`"
            f"**{EMOJI} Kanjeng:** {mention}\n",
        )


@kanjeng.alfareza_cmd(
    pattern="ialive$",
    command=("ialive", plugin_category),
    info={
        "header": "To check bot's alive status via inline mode",
        "options": "To show media in this cmd you need to set ALIVE_PIC with media link, get this by replying the media by .tgm",
        "usage": [
            "{tr}alive",
        ],
    },
)
async def amireallyalive(event):
    "A kind of showing bot details by your inline bot"
    reply_to_id = await reply_id(event)
    kanjeng_caption = f"**PetercordBot is Up and Running**\n"
    kanjeng_caption += f"**{EMOJI} Telethon version :** `{version.__version__}\n`"
    kanjeng_caption += f"**{EMOJI} Kanjeng Version :** `{kanjengversion}`\n"
    kanjeng_caption += f"**{EMOJI} Python Version :** `{python_version()}\n`"
    kanjeng_caption += f"**{EMOJI} Kanjeng:** {mention}\n"
    results = await event.client.inline_query(Config.TG_BOT_USERNAME, kanjeng_caption)
    await results[0].click(event.chat_id, reply_to=reply_to_id, hide_via=True)
    await event.delete()


@kanjeng.tgbot.on(CallbackQuery(data=re.compile(b"stats")))
async def on_plug_in_callback_query_handler(event):
    statstext = await petercordalive(StartTime)
    await event.answer(statstext, cache_time=0, alert=True)
