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

from plugins.download_aria_p_n import call_apropriate_function, aria_start


async def status_message_f(client, message):
    aria_i_p = await aria_start()
    # Show All Downloads
    downloads = aria_i_p.get_downloads()
    msg = ""
    for download in downloads:
        msg = msg + "File: `" + str(download.name) + "`\n"
        msg = msg + "Speed: " + str(download.download_speed_string()) + "\n"
        msg = msg + "Progress: " + str(download.progress_string(
        )) + "\n"
        msg = msg + "Total Size: " + str(download.total_length_string()) + "\n"
        msg = msg + "Status: " + str(download.status) + "\n"
        msg = msg + "ETA:  " + str(download.eta_string()) + "\n\n"
    LOGGER.info(msg)
    message.reply_text(msg, quote=True)


async def cancel_message_f(client, message):
    if len(message.command) > 1:
        aria_i_p = await aria_start()
        g_id = message.command[1].strip()
        LOGGER.info(g_id)
        downloads = aria_i_p.get_download(g_id)
        LOGGER.info(downloads)
        LOGGER.info(aria_i_p.pause(downloads))
        await message.reply_text(
            "Leech Cancelled",
            quote=True
        )
    else:
        await message.delete()
