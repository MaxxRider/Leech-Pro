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

import aiohttp

from tobrot import (
    TG_OFFENSIVE_API
)


async def extract_link(message, type_o_request):
    custom_file_name = None
    url = None

    if message is None:
        url = None
        custom_file_name = None

    elif message.text is not None:
        if message.text.lower().startswith("magnet:"):
            url = message.text.strip()

        elif "|" in message.text:
            url, custom_file_name = message.text.split("|")
            url = url.strip()
            custom_file_name = custom_file_name.strip()

        else:
            url = message.text.strip()

    elif message.document is not None:
        if message.document.file_name.lower().endswith(".torrent"):
            url = await message.download()
            custom_file_name = message.caption

    elif message.caption is not None:
        if "|" in message.caption:
            url, custom_file_name = message.caption.split("|")
            url = url.strip()
            custom_file_name = custom_file_name.strip()

        else:
            url = message.caption.strip()

    elif message.entities is not None:
        url = message.text

    # additional conditional check,
    # here to FILTER out BAD URLs
    LOGGER.info(TG_OFFENSIVE_API)
    if TG_OFFENSIVE_API is not None:
        try:
            async with aiohttp.ClientSession() as session:
                api_url = TG_OFFENSIVE_API.format(
                    i=url,
                    m=custom_file_name,
                    t=type_o_request
                )
                LOGGER.info(api_url)
                async with session.get(api_url) as resp:
                    suats = int(resp.status)
                    err = await resp.text()
                    if suats != 200:
                        url = None
                        custom_file_name = err
        except:
            # this might occur in case of a BAD API URL,
            # who knows? :\
            pass

    return url, custom_file_name
