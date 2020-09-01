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
    REAL_DEBRID_KEY
)


import aiohttp
import asyncio


BASE_URL = "https://api.real-debrid.com/rest/1.0"


async def fetch(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.json()


async def extract_it(restricted_link, custom_file_name):
    async with aiohttp.ClientSession() as session:
        url_to_send = BASE_URL + "/unrestrict/link?auth_token=" + REAL_DEBRID_KEY
        to_send_data = {
            "link": restricted_link
        }
        html = await fetch(session, url_to_send, to_send_data)
        LOGGER.info(html)
        downloadable_url = html.get("download")
        original_file_name = custom_file_name
        if original_file_name is None:
            original_file_name = html.get("filename")
        return downloadable_url, original_file_name
