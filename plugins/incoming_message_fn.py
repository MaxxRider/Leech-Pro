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


import time
from plugins.extract_link_from_message import extract_link
from plugins.real_debrid_extractor import extract_it
from plugins.download_from_link import request_download
from plugins.display_progress import progress_for_pyrogram


async def incoming_message_f(client, message):
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    dl_url, cf_name = extract_link(message.text)
    # LOGGER.info(dl_url)
    # LOGGER.info(cf_name)
    await i_m_sefg.edit_text("extracting links")
    downloadable_link, downloadable_file_name = await extract_it(dl_url, cf_name)
    # LOGGER.info(downloadable_link)
    # LOGGER.info(downloadable_file_name)
    dl_requested_user = message.from_user.id
    await i_m_sefg.edit_text("trying to download")
    sagtus, err_message = await request_download(
        downloadable_link,
        downloadable_file_name,
        dl_requested_user
    )
    if sagtus:
        await i_m_sefg.edit_text("downloaded.. now uploading ...")
        # upload file
        start_time = time.time()
        await client.send_document(
            chat_id=message.chat.id,
            document=err_message,
            caption=dl_url,
            parse_mode="html",
            disable_notification=True,
            reply_to_message_id=i_m_sefg.message_id,
            progress=progress_for_pyrogram,
            progress_args=(
                "trying to upload",
                i_m_sefg,
                start_time
            )
        )
        #
        await i_m_sefg.delete()
    else:
        await i_m_sefg.edit_text(err_message)
