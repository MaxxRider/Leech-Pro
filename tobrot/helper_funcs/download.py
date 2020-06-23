# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
#

import asyncio
import math
import os
import time
from datetime import datetime
from pySmartDL import SmartDL
from pyrogram import Client, Filters

from tobrot import (
    DOWNLOAD_LOCATION
)
from tobrot.helper_funcs.display_progress import progress_for_pyrogram
#from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive
from tobrot.helper_funcs.download_aria_p_n import call_apropriate_function_t

async def down_load_media_f(client, sms):
    message = await sms.reply_text("...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    is_unzip = False
    is_unrar = False
    is_untar = False
    if len(sms.command) > 1:
        if sms.command[1] == "unzip":
            is_unzip = True
        elif sms.command[1] == "unrar":
            is_unrar = True
        elif sms.command[1] == "untar":
            is_untar = True
    if sms.reply_to_message is not None:
        start_t = datetime.now()
        download_location = DOWNLOAD_LOCATION + "/"
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=sms.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                "trying to download", message, c_time
            )
        )
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        await message.edit(f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds")
        await call_apropriate_function_t(the_real_download_location, message, is_unzip, is_unrar, is_untar)
    elif len(sms.command) > 1:
        start_t = datetime.now()
        the_url_parts = " ".join(sms.command[1:])
        url = the_url_parts.strip()
        custom_file_name = os.path.basename(url)
        if "|" in the_url_parts:
            url, custom_file_name = the_url_parts.split("|")
            url = url.strip()
            custom_file_name = custom_file_name.strip()
        download_file_path = os.path.join(DOWNLOAD_LOCATION, custom_file_name)
        downloader = SmartDL(url, download_file_path, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        while not downloader.isFinished():
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            display_message = ""
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            elapsed_time = round(diff) * 1000
            progress_str = "[{0}{1}]\nProgress: {2}%".format(
                ''.join(["█" for i in range(math.floor(percentage / 5))]),
                ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
                round(percentage, 2))
            estimated_total_time = downloader.get_eta(human=True)
            try:
                current_message = f"trying to download\n"
                current_message += f"URL: {url}\n"
                current_message += f"File Name: {custom_file_name}\n"
                current_message += f"{progress_str}\n"
                current_message += f"{humanbytes(downloaded)} of {humanbytes(total_length)}\n"
                current_message += f"ETA: {estimated_total_time}"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await message.edit(
                        disable_web_page_preview=True,
                        text=current_message
                    )
                    display_message = current_message
                    await asyncio.sleep(10)
            except Exception as e:
                LOGGER.info(str(e))
                pass
        if os.path.exists(download_file_path):
            end_t = datetime.now()
            ms = (end_t - start_t).seconds
            await message.edit(f"Downloaded to <code>{download_file_path}</code> in <u>{ms}</u> seconds")
            await upload_to_gdrive(download_file_path, message)
    else:
        await message.edit("Reply to a Telegram Media, to download it to local server.")
