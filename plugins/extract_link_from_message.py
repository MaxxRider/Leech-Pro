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


def extract_link(message):
    custom_file_name = None
    url = None
    if message is None:
        url = None
        custom_file_name = None
    elif "|" in message.text:
        url, custom_file_name = message.text.split("|")
        url = url.strip()
        custom_file_name = custom_file_name.strip()
    elif message.entities is not None:
        url = message.text
    return url, custom_file_name
