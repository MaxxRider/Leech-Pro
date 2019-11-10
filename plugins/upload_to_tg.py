#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import asyncio
import os
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from plugins.display_progress import progress_for_pyrogram, humanbytes
from plugins.help_Nekmo_ffmpeg import take_screen_shot
from plugins.split_large_files import split_large_files

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config


async def upload_to_tg(message, local_file_name, from_user):
    LOGGER.info(local_file_name)
    caption_str = ""
    caption_str += "<code>"
    caption_str += os.path.basename(local_file_name)
    caption_str += "</code>"
    caption_str += "\n\n"
    caption_str += "<a href='tg://user?id="
    caption_str += str(from_user)
    caption_str += "'>"
    caption_str += "Here is the file to the link you sent"
    caption_str += "</a>"
    if os.path.isdir(local_file_name):
        directory_contents = os.listdir(local_file_name)
        new_m_esg = await message.reply_text(
            "Found {} files".format(len(directory_contents)),
            quote=True
            # reply_to_message_id=message.message_id
        )
        for single_file in directory_contents:
            # recursion: will this FAIL somewhere?
            await upload_to_tg(
                new_m_esg,
                os.path.join(local_file_name, single_file),
                from_user
            )
    else:
        if os.path.getsize(local_file_name) > Config.TG_MAX_FILE_SIZE:
            LOGGER.info("TODO")
            d_f_s = humanbytes(os.path.getsize(local_file_name))
            i_m_s_g = await message.reply_text(
                "Telegram does not support uploading this file."
                f"Detected File Size: {d_f_s} 😡"
                "🤖 trying to split the files 🌝🌝🌚"
            )
            splitted_dir = await split_large_files(local_file_name)
            totlaa_sleif = os.listdir(splitted_dir)
            totlaa_sleif.sort()
            LOGGER.info(totlaa_sleif)
            for le_file in totlaa_sleif:
                # recursion: will this FAIL somewhere?
                await upload_to_tg(
                    message,
                    os.path.join(splitted_dir, le_file),
                    from_user
                )
        else:
            await upload_single_file(message, local_file_name, caption_str)


async def upload_single_file(message, local_file_name, caption_str):
    await asyncio.sleep(5)
    start_time = time.time()
    try:
        if local_file_name.upper().endswith(("MKV", "MP4", "WEBM")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            #
            width = 0
            height = 0
            thumb_image_path = await take_screen_shot(
                local_file_name,
                os.path.dirname(os.path.abspath(local_file_name)),
                (duration / 2)
            )
            # get the correct width, height, and duration for videos greater than 10MB
            if os.path.exists(thumb_image_path):
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
                Image.open(thumb_image_path).convert(
                    "RGB"
                ).save(thumb_image_path)
                img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
                img.resize((320, height))
                img.save(thumb_image_path, "JPEG")
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            #
            thumb = None
            if os.path.exists(thumb_image_path):
                thumb = thumb_image_path
            # send video
            await message.reply_video(
                video=local_file_name,
                # quote=True,
                caption=caption_str,
                parse_mode="html",
                duration=duration,
                width=width,
                height=height,
                thumb=thumb,
                supports_streaming=True,
                disable_notification=True,
                reply_to_message_id=message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload",
                    message,
                    start_time
                )
            )
            os.remove(thumb)
        elif local_file_name.upper().endswith(("MP3", "M4A", "FLAC", "WAV")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            title = ""
            artist = ""
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("title"):
                title = metadata.get("title")
            if metadata.has("artist"):
                artist = metadata.get("artist")
            # send audio
            await message.reply_audio(
                audio=local_file_name,
                # quote=True,
                caption=caption_str,
                parse_mode="html",
                duration=duration,
                performer=artist,
                title=title,
                # thumb=,
                disable_notification=True,
                reply_to_message_id=message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload",
                    message,
                    start_time
                )
            )
        else:
            # send document
            await message.reply_document(
                document=local_file_name,
                # quote=True,
                # thumb=,
                caption=caption_str,
                parse_mode="html",
                disable_notification=True,
                reply_to_message_id=message.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    "trying to upload",
                    message,
                    start_time
                )
            )
    except Exception as e:
        await message.edit_text("**FAILED**\n" + str(e))
    else:
        await message.delete()
    os.remove(local_file_name)
