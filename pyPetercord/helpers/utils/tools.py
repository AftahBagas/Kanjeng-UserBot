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
        petercordevent = await edit_or_reply(
            event, f"`Transfiguration Time! Converting to ....`"
        )
    else:
        petercordevent = event
    petercordmedia = None
    petercordfile = os.path.join("./temp/", "meme.png")
    if os.path.exists(petercordfile):
        os.remove(petercordfile)
    if mediatype == "Photo":
        petercordmedia = await reply.download_media(file="./temp")
        im = Image.open(petercordmedia)
        im.save(petercordfile)
    elif mediatype in ["Audio", "Voice"]:
        await event.client.download_media(reply, petercordfile, thumb=-1)
    elif mediatype == "Sticker":
        petercordmedia = await reply.download_media(file="./temp")
        if petercordmedia.endswith(".tgs"):
            await runcmd(
                f"lottie_convert.py --frame 0 -if lottie -of png '{petercordmedia}' '{petercordfile}'"
            )
        elif petercordmedia.endswith(".webp"):
            im = Image.open(petercordmedia)
            im.save(petercordfile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        await event.client.download_media(reply, petercordfile, thumb=-1)
        if not os.path.exists(petercordfile):
            petercordmedia = await reply.download_media(file="./temp")
            clip = VideoFileClip(media)
            try:
                clip = clip.save_frame(petercordfile, 0.1)
            except:
                clip = clip.save_frame(petercordfile, 0)
    elif mediatype == "Document":
        mimetype = reply.document.mime_type
        mtype = mimetype.split("/")
        if mtype[0].lower() == "image":
            petercordmedia = await reply.download_media(file="./temp")
            im = Image.open(petercordmedia)
            im.save(petercordfile)
    if petercordmedia and os.path.exists(petercordmedia):
        os.remove(petercordmedia)
    if os.path.exists(petercordfile):
        return petercordevent, petercordfile, mediatype
    return petercordevent, None


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
