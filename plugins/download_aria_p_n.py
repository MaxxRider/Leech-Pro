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

import aria2p
import asyncio
import os
from plugins.upload_to_tg import upload_to_tg

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config


async def aria_start():
    aria2_daemon_start_cmd = []
    # start the daemon, aria2c command
    aria2_daemon_start_cmd.append("aria2c")
    aria2_daemon_start_cmd.append("--allow-overwrite=true")
    aria2_daemon_start_cmd.append("--daemon=true")
    # aria2_daemon_start_cmd.append(f"--dir={Config.TMP_DOWNLOAD_DIRECTORY}")
    # TODO: this does not work, need to investigate this.
    # but for now, https://t.me/TrollVoiceBot?start=858
    aria2_daemon_start_cmd.append("--enable-rpc")
    aria2_daemon_start_cmd.append("--follow-torrent=mem")
    aria2_daemon_start_cmd.append("--max-connection-per-server=10")
    aria2_daemon_start_cmd.append("--min-split-size=10M")
    aria2_daemon_start_cmd.append("--rpc-listen-all=false")
    aria2_daemon_start_cmd.append(f"--rpc-listen-port={Config.ARIA_TWO_STARTED_PORT}")
    aria2_daemon_start_cmd.append("--rpc-max-request-size=1024M")
    aria2_daemon_start_cmd.append("--seed-ratio=100.0")
    aria2_daemon_start_cmd.append("--seed-time=1")
    aria2_daemon_start_cmd.append("--split=10")
    #
    LOGGER.info(aria2_daemon_start_cmd)
    #
    process = await asyncio.create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    LOGGER.info(stdout)
    LOGGER.info(stderr)
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=Config.ARIA_TWO_STARTED_PORT,
            secret=""
        )
    )
    return aria2


def add_magnet(aria_instance, magnetic_link, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    try:
        download = aria_instance.add_magnet(
            magnetic_link,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    else:
        return True, "" + download.gid + ""


def add_url(aria_instance, text_url, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    uris = [text_url]
    # Add URL Into Queue
    try:
        download = aria_instance.add_uris(
            uris,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    else:
        return True, "" + download.gid + ""


async def call_apropriate_function(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p
):
    if incoming_link.startswith("magnet:"):
        sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name)
    else:
        sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name)
    if not sagtus:
        return sagtus, err_message
    LOGGER.info(err_message)
    await check_progress_for_dl(
        aria_instance,
        err_message,
        sent_message_to_update_tg_p
    )
    if incoming_link.startswith("magnet:"):
        #
        err_message = await check_metadata(aria_instance, err_message)
        await check_progress_for_dl(
            aria_instance,
            err_message,
            sent_message_to_update_tg_p
        )
    file = aria_instance.get_download(err_message)
    await upload_to_tg(
        sent_message_to_update_tg_p,
        file.name,
        sent_message_to_update_tg_p.reply_to_message.from_user.id
    )
    return True, None


async def check_progress_for_dl(aria2, gid, event):
    complete = None
    previous_message = None
    while not complete:
        file = aria2.get_download(gid)
        complete = file.is_complete
        try:
            if not file.error_message:
                msg = f"\nDownloading File: `{file.name}`"
                msg += f"\nSpeed: {file.download_speed_string()} 🔽 / {file.upload_speed_string()} 🔼"
                msg += f"\nProgress: {file.progress_string()}"
                msg += f"\nTotal Size: {file.total_length_string()}"
                msg += f"\nStatus: {file.status}"
                msg += f"\nETA: {file.eta_string()}"
                msg += f"\n`/cancel {gid}`"
                LOGGER.info(msg)
                if msg != previous_message:
                    await event.edit(msg)
                    previous_message = msg
                    await asyncio.sleep(Config.EDIT_SLEEP_TIME_OUT)
            else:
                msg = file.error_message
                await event.edit(f"`{msg}`")
                return False
        except Exception as e:
            LOGGER.info(str(e))
            pass
    file = aria2.get_download(gid)
    complete = file.is_complete
    if complete:
        await event.edit(f"File Downloaded Successfully: `{file.name}`")


async def check_metadata(aria2, gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    LOGGER.info("Changing GID " + gid + " to " + new_gid)
    return new_gid
