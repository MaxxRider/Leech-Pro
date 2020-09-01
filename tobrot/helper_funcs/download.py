#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52 | Shrimadhav U K

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
import re
import time
import subprocess
from datetime import datetime
from pyrogram import Client, filters

from tobrot import (
    DOWNLOAD_LOCATION
)
from tobrot.helper_funcs.display_progress_g import progress_for_pyrogram_g
from tobrot.helper_funcs.upload_to_tg import upload_to_gdrive
from tobrot.helper_funcs.download_aria_p_n import call_apropriate_function_t
from tobrot.helper_funcs.create_compressed_archive import unzip_me, unrar_me, untar_me

async def down_load_media_f(client, message):
    user_id = message.from_user.id
    print(user_id)
    mess_age = await message.reply_text("...", quote=True)
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    if message.reply_to_message is not None:
        start_t = datetime.now()
        download_location = "/app/"
        c_time = time.time()
        the_real_download_location = await client.download_media(
            message=message.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram_g,
            progress_args=(
                "trying to download", mess_age, c_time
            )
        )
        end_t = datetime.now()
        ms = (end_t - start_t).seconds
        LOGGER.info(the_real_download_location)
        await asyncio.sleep(10)
        await mess_age.edit_text(f"Downloaded to <code>{the_real_download_location}</code> in <u>{ms}</u> seconds")
        the_real_download_location_g = os.path.basename(the_real_download_location)
        LOGGER.info(the_real_download_location_g)
        if len(message.command) > 1:
            if message.command[1] == "unzip":
                file_upload = await unzip_me(the_real_download_location_g)
                if file_upload is not None:
                    g_response = await upload_to_gdrive(file_upload, mess_age, message, user_id)
                    LOGGER.info(g_response)
                    
            elif message.command[1] == "unrar":
                file_uploade = await unrar_me(the_real_download_location_g)
                if file_uploade is not None:
                    gk_response = await upload_to_gdrive(file_uploade, mess_age, message, user_id)
                    LOGGER.info(gk_response)
                    
            elif message.command[1] == "untar":
                 file_uploadg = await untar_me(the_real_download_location_g)
                 if file_uploadg is not None:
                     gau_response = await upload_to_gdrive(file_uploadg, mess_age, message, user_id)
                     LOGGER.info(gau_response)
        else:
            gaut_response = await upload_to_gdrive(the_real_download_location_g, mess_age, message, user_id)
            LOGGER.info(gaut_response)
    else:
        #await asyncio.sleep(4)
        await mess_age.edit_text("Reply to a Telegram Media, to upload to the Cloud Drive.")
