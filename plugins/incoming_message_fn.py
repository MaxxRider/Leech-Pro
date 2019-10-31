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
from plugins.extract_link_from_message import extract_link
from plugins.download_aria_p_n import call_apropriate_function, aria_start
from plugins.download_from_link import request_download
from plugins.display_progress import progress_for_pyrogram


async def incoming_message_f(client, message):
    i_m_sefg = await message.reply_text("processing", quote=True)
    LOGGER.info(message)
    dl_url, cf_name = extract_link(message.reply_to_message)
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        aria_i_p = aria_start()
        LOGGER.info(aria_i_p)
        await i_m_sefg.edit_text("trying to download")
        sagtus, err_message = await call_apropriate_function(
            aria_i_p,
            dl_url,
            cf_name,
            i_m_sefg
        )
        if not sagtus:
            await i_m_sefg.edit_text(err_message)
    else:
        await i_m_sefg.edit_text("**FCUK**! wat have you entered. Please read /help")
