#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import os
import io
import sys
import traceback

from tobrot import (
    DOWNLOAD_LOCATION,
    TG_BOT_TOKEN,
    APP_ID,
    API_HASH,
    AUTH_CHANNEL,
    LEECH_COMMAND,
    YTDL_COMMAND,
    GLEECH_COMMAND,
    TELEGRAM_LEECH_COMMAND_G
)

from pyrogram import Client, Filters, MessageHandler, CallbackQueryHandler

from tobrot.plugins.new_join_fn import new_join_f, help_message_f, rename_message_f
from tobrot.plugins.incoming_message_fn import incoming_message_f, incoming_youtube_dl_f, incoming_purge_message_f, incoming_gdrive_message_f
from tobrot.plugins.status_message_fn import (
    status_message_f,
    cancel_message_f,
    exec_message_f,
    upload_document_f
    #eval_message_f
)
from tobrot.plugins.call_back_button_handler import button
from tobrot.plugins.custom_thumbnail import (
    save_thumb_nail,
    clear_thumb_nail
)
from tobrot.helper_funcs.download import down_load_media_f


if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(DOWNLOAD_LOCATION):
        os.makedirs(DOWNLOAD_LOCATION)
    #
    app = Client(
        "LeechBot",
        bot_token=TG_BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        workers=343
    )
    #
    incoming_message_handler = MessageHandler(
        incoming_message_f,
        filters=Filters.command([f"{LEECH_COMMAND}"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_message_handler)
    #
    incoming_gdrive_message_handler = MessageHandler(
        incoming_gdrive_message_f,
        filters=Filters.command([f"{GLEECH_COMMAND}"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_gdrive_message_handler)
    #
    incoming_telegram_download_handler = MessageHandler(
        down_load_media_f,
        filters=Filters.command([f"{TELEGRAM_LEECH_COMMAND_G}"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_telegram_download_handler)
    #
    incoming_purge_message_handler = MessageHandler(
        incoming_purge_message_f,
        filters=Filters.command(["purge"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_purge_message_handler)
    #
    incoming_youtube_dl_handler = MessageHandler(
        incoming_youtube_dl_f,
        filters=Filters.command([f"{YTDL_COMMAND}"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(incoming_youtube_dl_handler)
    #
    status_message_handler = MessageHandler(
        status_message_f,
        filters=Filters.command(["status"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(status_message_handler)
    #
    cancel_message_handler = MessageHandler(
        cancel_message_f,
        filters=Filters.command(["cancel"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(cancel_message_handler)
    #
    exec_message_handler = MessageHandler(
        exec_message_f,
        filters=Filters.command(["exec"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(exec_message_handler)
    #
    '''
    eval_message_handler = MessageHandler(
        eval_message_f,
        filters=Filters.command(["eval"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(eval_message_handler)
    '''
    #
    rename_message_handler = MessageHandler(
        rename_message_f,
        filters=Filters.command(["rename"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(rename_message_handler)
    #
    upload_document_handler = MessageHandler(
        upload_document_f,
        filters=Filters.command(["upload@MaxxLeechPro_Bot"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(upload_document_handler)

    help_text_handler = MessageHandler(
        help_message_f,
        filters=Filters.command(["help@MaxxLeechPro_Bot"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(help_text_handler)
    #
    new_join_handler = MessageHandler(
        new_join_f,
        filters=~Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(new_join_handler)
    #
    group_new_join_handler = MessageHandler(
        help_message_f,
        filters=Filters.chat(chats=AUTH_CHANNEL) & Filters.new_chat_members
    )
    app.add_handler(group_new_join_handler)
    #
    call_back_button_handler = CallbackQueryHandler(
        button
    )
    app.add_handler(call_back_button_handler)
    #
    save_thumb_nail_handler = MessageHandler(
        save_thumb_nail,
        filters=Filters.command(["savethumbnail@MaxxLeechPro_Bot"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(save_thumb_nail_handler)
    #
    clear_thumb_nail_handler = MessageHandler(
        clear_thumb_nail,
        filters=Filters.command(["clearthumbnail@MaxxLeechPro_Bot"]) & Filters.chat(chats=AUTH_CHANNEL)
    )
    app.add_handler(clear_thumb_nail_handler)
    #
    app.run()
