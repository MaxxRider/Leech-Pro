#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

# the logging things
import logging
import os
import shutil
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

from pyrogram.types import CallbackQuery
from tobrot.helper_funcs.admin_check import AdminCheck
from tobrot.helper_funcs.download_aria_p_n import aria_start
from tobrot.helper_funcs.youtube_dl_button import youtube_dl_call_back
from tobrot.plugins.status_message_fn import cancel_message_f
from tobrot import (
    MAX_MESSAGE_LENGTH,
    AUTH_CHANNEL
)
async def button(bot, update: CallbackQuery):
    cb_data = update.data
    try:
        g = await AdminCheck(bot, update.message.chat.id, update.from_user.id)
        print(g)
    except:
        pass
    if "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    elif (update.from_user.id == update.message.reply_to_message.from_user.id) or g:
        print(cb_data)
        if cb_data.startswith("cancel"):
            if len(cb_data) > 1:
                i_m_s_e_g = await update.message.reply_text("checking..?", quote=True)
                aria_i_p = await aria_start()
                g_id = cb_data.split()[-1]
                LOGGER.info(g_id)
                try:
                    downloads = aria_i_p.get_download(g_id)
                    file_name = downloads.name
                    LOGGER.info(downloads)
                    LOGGER.info(downloads.remove(force=True))
                    if os.path.exists(file_name):
                        if os.path.isdir(file_name):
                            shutil.rmtree(file_name)
                        else:
                            os.remove(file_name)
                    await i_m_s_e_g.edit_text(f"Leech Cancelled by <a href='tg://user?id={update.from_user.id}'>{update.from_user.first_name}</a>")
                except Exception as e:
                    await i_m_s_e_g.edit_text("<i>FAILED</i>\n\n" + str(e) + "\n#error")
                else:
                    await update.message.delete()
        elif cb_data == "fuckingdo":
            if update.from_user.id in AUTH_CHANNEL:
                g_d_list = ['app.json', 'venv', 'rclone.conf', '.gitignore', '_config.yml', 'COPYING', 'Dockerfile', 'DOWNLOADS', 'Procfile', '.heroku', '.profile.d', 'rclone.jpg', 'README.md', 'requirements.txt', 'runtime.txt', 'start.sh', 'tobrot', 'gautam', 'Torrentleech-Gdrive.log', 'vendor']
                LOGGER.info(g_d_list)
                g_list = os.listdir()
                LOGGER.info(g_list)
                g_del_list = list(set(g_list)-set(g_d_list))
                LOGGER.info(g_del_list)
                if len(g_del_list) != 0:
                    for f in g_del_list:
                        if os.path.isfile(f):
                            os.remove(f)
                        else:
                            shutil.rmtree(f)
                    await update.message.edit_text(f"Deleted {len(g_del_list)} objects 😬")
                else:
                    await update.message.edit_text("Nothing to clear 🙄")
            else:
                await update.message.edit_text("You are not allowed to do that 🤭")
        elif cb_data == "fuckoff":
            await update.message.edit_text("Okay! fine 🤬")
				
