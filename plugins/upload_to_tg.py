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


import os
import time
from plugins.display_progress import progress_for_pyrogram


async def upload_to_tg(message, local_file_name):
    LOGGER.info(local_file_name)
    caption_str += "<code>"
    caption_str = os.path.basename(local_file_name)
    caption_str += "</code>"
    caption_str += "\n\n"
    caption_str += "<a href='tg://user?id=" + message.reply_to_message.from_user.id + "'>"
    caption_str += "Here is the file to the link you sent"
    caption_str += "</a>"
    start_time = time.time()
    try:
        if local_file_name.upper().endswith(("MKV", "MP4", "WEBM")):
            # send video
            await message.reply_video(
                video=local_file_name,
                # quote=True,
                caption=caption_str,
                parse_mode="html",
                # duration=,
                # width=,
                # height=,
                # thumb=,
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
            # send audio
            await message.reply_audio(
                audio=local_file_name,
                # quote=True,
                caption=caption_str,
                parse_mode="html",
                # duration=,
                # performer=,
                # title=,
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
        await message.edit_text("Process Completed")
    os.remove(local_file_name)
