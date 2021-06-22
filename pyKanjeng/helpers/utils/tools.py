import os
from typing import Optional

from moviepy.editor import VideoFileClip
from PIL import Image

from ...core.logger import logging
from ...core.managers import edit_or_reply
from ..tools import media_type
from .utils import runcmd

LOGS = logging.getLogger(__name__)


async def media_to_pic(event, reply, noedits=False):
    mediatype = media_type(reply)
    if mediatype not in [
        "Photo",
        "Round Video",
        "Gif",
        "Sticker",
        "Video",
        "Voice",
        "Audio",
        "Document",
    ]:
        return event, None
    if not noedits:
        kanjengevent = await edit_or_reply(
            event, f"`Transfiguration Time! Converting to ....`"
        )
    else:
        kanjengevent = event
    kanjengmedia = None
    kanjengfile = os.path.join("./temp/", "meme.png")
    if os.path.exists(kanjengfile):
        os.remove(kanjengfile)
    if mediatype == "Photo":
        kanjengmedia = await reply.download_media(file="./temp")
        im = Image.open(petercordmedia)
        im.save(kanjengfile)
    elif mediatype in ["Audio", "Voice"]:
        await event.client.download_media(reply, petercordfile, thumb=-1)
    elif mediatype == "Sticker":
        kanjengmedia = await reply.download_media(file="./temp")
        if kanjengmedia.endswith(".tgs"):
            await runcmd(
                f"lottie_convert.py --frame 0 -if lottie -of png '{petercordmedia}' '{petercordfile}'"
            )
        elif kanjengmedia.endswith(".webp"):
            im = Image.open(kanjengmedia)
            im.save(petercordfile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        await event.client.download_media(reply, petercordfile, thumb=-1)
        if not os.path.exists(kanjengfile):
            kanjengmedia = await reply.download_media(file="./temp")
            clip = VideoFileClip(media)
            try:
                clip = clip.save_frame(kanjengfile, 0.1)
            except:
                clip = clip.save_frame(kanjengfile, 0)
    elif mediatype == "Document":
        mimetype = reply.document.mime_type
        mtype = mimetype.split("/")
        if mtype[0].lower() == "image":
            kanjengmedia = await reply.download_media(file="./temp")
            im = Image.open(kanjengmedia)
            im.save(kanjengfile)
    if kanjengmedia and os.path.exists(petercordmedia):
        os.remove(kanjengmedia)
    if os.path.exists(kanjengfile):
        return kanjengevent, kanjengfile, mediatype
    return kanjengevent, None


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    thumb_image_path = path or os.path.join(
        "./temp/", f"{os.path.basename(video_file)}.jpg"
    )
    command = f"ffmpeg -ss {duration} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
