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

from tobrot import (
    DOWNLOAD_LOCATION
)


import time
from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.download_aria_p_n import call_apropriate_function, aria_start
from tobrot.helper_funcs.download_from_link import request_download
from tobrot.helper_funcs.display_progress import progress_for_pyrogram
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats


async def incoming_message_f(client, message):
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    dl_url, cf_name = extract_link(message.reply_to_message)
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        aria_i_p = await aria_start()
        LOGGER.info(aria_i_p)
        new_download_location = os.path.join(
            DOWNLOAD_LOCATION,
            str(time.time()),
            cf_name if cf_name is not None else ""
        )
        # create download directory, if not exist
        if not os.path.isdir(new_download_location):
            os.makedirs(new_download_location)
        await i_m_sefg.edit_text("trying to download")
        sagtus, err_message = await call_apropriate_function(
            aria_i_p,
            dl_url,
            new_download_location,
            i_m_sefg
        )
        if not sagtus:
            await i_m_sefg.edit_text(err_message)
    else:
        await i_m_sefg.edit_text("**FCUK**! wat have you entered. Please read /help")


async def incoming_youtube_dl_f(client, message):
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    dl_url, cf_name = extract_link(message.reply_to_message)
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.from_user.id
        user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
        # create download directory, if not exist
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)
        text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url,
            user_working_dir
        )
        await i_m_sefg.edit_text(
            text=text_message,
            reply_markup=reply_markup
        )
