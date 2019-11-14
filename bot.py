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

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from pyrogram import Client, Filters, MessageHandler, CallbackQueryHandler
from plugins.new_join_fn import new_join_f, help_message_f, rename_message_f
from plugins.incoming_message_fn import incoming_message_f, incoming_youtube_dl_f
from plugins.status_message_fn import status_message_f, cancel_message_f
from plugins.call_back_button_handler import button


if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    #
    app = Client(
        "LeechBot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        workers=343
    )
    #
    incoming_message_handler = MessageHandler(
        incoming_message_f,
        filters=Filters.command(["leech"]) & Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(incoming_message_handler)
    #
    incoming_youtube_dl_handler = MessageHandler(
        incoming_youtube_dl_f,
        filters=Filters.command(["ytdl"]) & Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(incoming_youtube_dl_handler)
    #
    status_message_handler = MessageHandler(
        status_message_f,
        filters=Filters.command(["status"]) & Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(status_message_handler)
    #
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=Filters.command(["cancel"]) & Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(cancel_message_handler)
    #
    rename_message_handler = MessageHandler(
        rename_message_f,
        filters=Filters.command(["rename"]) & Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(rename_message_handler)

    help_text_handler = MessageHandler(
        help_message_f,
        filters=Filters.command(["help"]) & Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(help_text_handler)
    #
    new_join_handler = MessageHandler(
        new_join_f,
        filters=~Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(new_join_handler)
    #
    group_new_join_handler = MessageHandler(
        help_message_f,
        filters=Filters.chat(chats=Config.AUTH_CHANNEL) & Filters.new_chat_members
    )
    app.add_handler(group_new_join_handler)
    #
    call_back_button_handler = CallbackQueryHandler(
        button
    )
    app.add_handler(call_back_button_handler)
    #
    app.run()
