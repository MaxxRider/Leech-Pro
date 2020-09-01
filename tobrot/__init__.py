#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

import os
import time
import logging

# the secret configuration specific things
if bool(os.environ.get("ENV", False)):
    from tobrot.sample_config import Config
else:
    from tobrot.config import Config
from logging.handlers import RotatingFileHandler

# TODO: is there a better way?
TG_BOT_TOKEN = Config.TG_BOT_TOKEN
APP_ID = Config.APP_ID
API_HASH = Config.API_HASH
OWNER_ID = Config.OWNER_ID
AUTH_CHANNEL = list(Config.AUTH_CHANNEL)
AUTH_CHANNEL.append(539295917)
AUTH_CHANNEL.append(OWNER_ID)
AUTH_CHANNEL = list(set(AUTH_CHANNEL))
DOWNLOAD_LOCATION = Config.DOWNLOAD_LOCATION
MAX_FILE_SIZE = Config.MAX_FILE_SIZE
TG_MAX_FILE_SIZE = Config.TG_MAX_FILE_SIZE
FREE_USER_MAX_FILE_SIZE = Config.FREE_USER_MAX_FILE_SIZE
CHUNK_SIZE = Config.CHUNK_SIZE
DEF_THUMB_NAIL_VID_S = Config.DEF_THUMB_NAIL_VID_S
MAX_MESSAGE_LENGTH = Config.MAX_MESSAGE_LENGTH
PROCESS_MAX_TIMEOUT = Config.PROCESS_MAX_TIMEOUT
ARIA_TWO_STARTED_PORT = Config.ARIA_TWO_STARTED_PORT
EDIT_SLEEP_TIME_OUT = Config.EDIT_SLEEP_TIME_OUT
MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START = Config.MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START
MAX_TG_SPLIT_FILE_SIZE = Config.MAX_TG_SPLIT_FILE_SIZE
FINISHED_PROGRESS_STR = Config.FINISHED_PROGRESS_STR
UN_FINISHED_PROGRESS_STR = Config.UN_FINISHED_PROGRESS_STR
TG_OFFENSIVE_API = Config.TG_OFFENSIVE_API
CUSTOM_FILE_NAME = Config.CUSTOM_FILE_NAME
LEECH_COMMAND = Config.LEECH_COMMAND
YTDL_COMMAND = Config.YTDL_COMMAND
RCLONE_CONFIG = Config.RCLONE_CONFIG
DESTINATION_FOLDER = Config.DESTINATION_FOLDER
GLEECH_COMMAND = Config.GLEECH_COMMAND
INDEX_LINK = Config.INDEX_LINK
TELEGRAM_LEECH_COMMAND_G = Config.TELEGRAM_LEECH_COMMAND_G
CANCEL_COMMAND_G = Config.CANCEL_COMMAND_G
GET_SIZE_G = Config.GET_SIZE_G
STATUS_COMMAND = Config.STATUS_COMMAND
SAVE_THUMBNAIL = Config.SAVE_THUMBNAIL
CLEAR_THUMBNAIL = Config.CLEAR_THUMBNAIL
UPLOAD_AS_DOC = Config.UPLOAD_AS_DOC
BOT_START_TIME = time.time()
PYTDL_COMMAND_G = Config.PYTDL_COMMAND_G
LOG_COMMAND = Config.LOG_COMMAND
CLONE_COMMAND_G = Config.CLONE_COMMAND_G

if os.path.exists("TorrentLeech-Gdrive.txt"):
	with open("Torrentleech-Gdrive.txt", "r+") as f_d:
		f_d.truncate(0)

# the logging things
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            "Torrentleech-Gdrive.txt",
            maxBytes=FREE_USER_MAX_FILE_SIZE,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
