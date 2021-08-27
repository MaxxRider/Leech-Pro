import logging

import pyrogram
from tobrot import *

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def new_join_f(client, message):
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(
            f"""<b>🙋🏻‍♂️ Hello dear!\n\n This Is A Leech Bot .This Chat Is Not Supposed To Use Me</b>\n\n<b>Current CHAT ID: <code>{message.chat.id}</code>""",
            parse_mode="html",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Channel', url='https://t.me/MaxxBots')
                    ]
                ]
               )
            )
        # leave chat
        await client.leave_chat(chat_id=message.chat.id, delete=True)
    # delete all other messages, except for AUTH_CHANNEL
    await message.delete(revoke=True)


async def help_message_f(client, message):
    if UPLOAD_AS_DOC:
        utxt = "Document"
    else:
        utxt = "Streamable"
    await message.reply_text(
        f"""Available Commands
/{RCLONE_COMMAND} : This will change your drive config on fly.(First one will be default)
 
/{CLONE_COMMAND_G}: This command is used to clone gdrive files or folder using gclone.
Syntax:- `[ID of the file or folder][one space][name of your folder only(If the id is of file, don't put anything)]` and then reply /gclone to it.
 
/{LOG_COMMAND}: This will send you a txt file of the logs.
 
/{YTDL_COMMAND}: This command should be used as reply to a supported link
 
/{PYTDL_COMMAND}: This command will download videos from youtube playlist link and will upload to telegram.
 
/{GYTDL_COMMAND}: This will download and upload to your cloud.
 
/{GPYTDL_COMMAND}: This download youtube playlist and upload to your cloud.
 
/{LEECH_COMMAND}: This command should be used as reply to a magnetic link, a torrent link, or a direct link. [this command will SPAM the chat and send the downloads a seperate files, if there is more than one file, in the specified torrent]
 
/{LEECH_ZIP_COMMAND}: This command should be used as reply to a magnetic link, a torrent link, or a direct link. [This command will create a .tar.gz file of the output directory, and send the files in the chat, splited into PARTS of 1024MiB each, due to Telegram limitations]
 
/{GLEECH_COMMAND}: This command should be used as reply to a magnetic link, a torrent link, or a direct link. And this will download the files from the given link or torrent and will upload to the cloud using rclone.
 
/{GLEECH_ZIP_COMMAND} This command will compress the folder/file and will upload to your cloud.
 
/{LEECH_UNZIP_COMMAND}: This will unarchive file and upload to telegram.
 
/{GLEECH_UNZIP_COMMAND}: This will unarchive file and upload to cloud.
 
/{TELEGRAM_LEECH_COMMAND}: This will mirror the telegram files to ur respective cloud .
 
/{TELEGRAM_LEECH_UNZIP_COMMAND}: This will unarchive telegram file and upload to cloud.
 
/{GET_SIZE_G}: This will give you total size of your destination folder in cloud.
 
/{RENEWME_COMMAND}: This will clear the remains of downloads which are not getting deleted after upload of the file or after /cancel command.
 
/{CANCEL_COMMAND_G} [GID]: To cancel ur download

/{RENAME_COMMAND}: To rename the telegram files.
 
Only work with direct link and youtube link for nowIt is like u can add custom name as prefix of the original file name. Like if your file name is gk.txt uploaded will be what u add in CUSTOM_FILE_NAME + gk.txt
 
Only works with direct link/youtube link.No magnet or torrent.
 
And also added custom name like...
 
You have to pass link as www.download.me/gk.txt | new.txt
 
the file will be uploaded as new.txt.
 
/{SAVE_THUMBNAIL}: Reply To A Photo To Save As Custom Thumbnail

/{CLEAR_THUMBNAIL}: To Clear Saved Custom Thumbnail

/{TOGGLE_VID}: To Upload Your Files As Streamable

/{TOGGLE_DOC}: To Upload Your Files As Documents

**How to Use....?**
__Send any one of the available command, as a reply to a valid link/magnet/torrent. 👊__

**Current Custom Upload Mode:** `{utxt}`

""",
        disable_web_page_preview=True,
    )
