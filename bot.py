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

from pyrogram import Client, Filters, MessageHandler
from plugins.new_join_fn import new_join_f
from plugins.incoming_message_fn import incoming_message_f


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
        filters=Filters.incoming & Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(incoming_message_handler)
    #
    new_join_handler = MessageHandler(
        new_join_f,
        filters=~Filters.chat(chats=Config.AUTH_CHANNEL)
    )
    app.add_handler(new_join_handler)
    #
    app.run()
