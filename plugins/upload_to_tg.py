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
from plugins.display_progress import progress_for_pyrogram


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
            thumb_image_path = "./thumb_image.jpg"
            thumb = None
            if os.path.exists(thumb_image_path):
                thumb = thumb_image_path
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
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
