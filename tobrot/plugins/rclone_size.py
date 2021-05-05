#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52
import asyncio
import logging
import os
import re
import subprocess

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tobrot import DESTINATION_FOLDER, EDIT_SLEEP_TIME_OUT, LOGGER, RCLONE_CONFIG


async def check_size_g(client, message):
    # await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    del_it = await message.reply_text("🔊 Checking size...wait!!!")
    if not os.path.exists("rclone.conf"):
        with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
            fole.write(f"{RCLONE_CONFIG}")
    if os.path.exists("rclone.conf"):
        with open("rclone.conf", "r+") as file:
            con = file.read()
            gUP = re.findall("\[(.*)\]", con)[0]
            LOGGER.info(gUP)
    destination = f"{DESTINATION_FOLDER}"
    cmd = ["rclone", "size", "--config=./rclone.conf", f"{gUP}:{destination}"]
    gau_tam = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    gau, tam = await gau_tam.communicate()
    LOGGER.info(gau)
    LOGGER.info(tam)
    LOGGER.info(tam.decode("utf-8"))
    gautam = gau.decode("utf-8")
    LOGGER.info(gautam)
    await asyncio.sleep(5)
    await message.reply_text(f"🔊CloudInfo:\n\n{gautam}")
    await del_it.delete()


# gautamajay52


async def g_clearme(client, message):
    inline_keyboard = []
    ikeyboard = []
    ikeyboard.append(
        InlineKeyboardButton("Yes 🚫", callback_data=("fuckingdo").encode("UTF-8"))
    )
    ikeyboard.append(
        InlineKeyboardButton("No 🤗", callback_data=("fuckoff").encode("UTF-8"))
    )
    inline_keyboard.append(ikeyboard)
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    await message.reply_text(
        "Are you sure? 🚫 This will delete all your downloads locally 🚫",
        reply_markup=reply_markup,
        quote=True,
    )
