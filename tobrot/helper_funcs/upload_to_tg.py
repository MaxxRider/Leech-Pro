#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52
 
import asyncio
import logging
import os
import re
import shutil
import subprocess
import time
from functools import partial
from pathlib import Path
 
import pyrogram.types as pyrogram
import requests
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from hurry.filesize import size
from PIL import Image
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.types import InputMediaAudio, InputMediaDocument, InputMediaVideo
from requests.utils import requote_uri
from tobrot import (
    DESTINATION_FOLDER,
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT,
    INDEX_LINK,
    LOGGER,
    RCLONE_CONFIG,
    TG_MAX_FILE_SIZE,
    UPLOAD_AS_DOC,
    gDict,
)
from tobrot.helper_funcs.copy_similar_file import copy_file
from tobrot.helper_funcs.display_progress import humanbytes, Progress
from tobrot.helper_funcs.help_Nekmo_ffmpeg import take_screen_shot
from tobrot.helper_funcs.split_large_files import split_large_files
 
# stackoverflow🤐
def getFolderSize(p):
    prepend = partial(os.path.join, p)
    return sum(
        [
            (os.path.getsize(f) if os.path.isfile(f) else getFolderSize(f))
            for f in map(prepend, os.listdir(p))
        ]
    )
 
 
async def upload_to_tg(
    message,
    local_file_name,
    from_user,
    dict_contatining_uploaded_files,
    client,
    edit_media=False,
    yt_thumb=None,
):
    base_file_name = os.path.basename(local_file_name)
    caption_str = ""
    caption_str += "<code>"
    caption_str += base_file_name
    caption_str += "</code>"
    if os.path.isdir(local_file_name):
        directory_contents = os.listdir(local_file_name)
        directory_contents.sort()
        # number_of_files = len(directory_contents)
        LOGGER.info(directory_contents)
        new_m_esg = message
        if not message.photo:
            new_m_esg = await message.reply_text(
                f"Found {len(directory_contents)} files <a href='tg://user?id={from_user}'>🤒</a>",
                quote=True
                # reply_to_message_id=message.message_id
            )
        for single_file in directory_contents:
            # recursion: will this FAIL somewhere?
            await upload_to_tg(
                new_m_esg,
                os.path.join(local_file_name, single_file),
                from_user,
                dict_contatining_uploaded_files,
                client,
                edit_media,
                yt_thumb,
            )
    else:
        if os.path.getsize(local_file_name) > TG_MAX_FILE_SIZE:
            LOGGER.info("TODO")
            d_f_s = humanbytes(os.path.getsize(local_file_name))
            i_m_s_g = await message.reply_text(
                "Telegram does not support uploading this file.\n"
                f"Detected File Size: {d_f_s} 😡\n"
                "\n🤖 trying to split the files 🌝🌝🌚"
            )
            splitted_dir = await split_large_files(local_file_name)
            totlaa_sleif = os.listdir(splitted_dir)
            totlaa_sleif.sort()
            number_of_files = len(totlaa_sleif)
            LOGGER.info(totlaa_sleif)
            ba_se_file_name = os.path.basename(local_file_name)
            await i_m_s_g.edit_text(
                f"Detected File Size: {d_f_s} 😡\n"
                f"<code>{ba_se_file_name}</code> splitted into {number_of_files} files.\n"
                "trying to upload to Telegram, now ..."
            )
            for le_file in totlaa_sleif:
                # recursion: will this FAIL somewhere?
                await upload_to_tg(
                    message,
                    os.path.join(splitted_dir, le_file),
                    from_user,
                    dict_contatining_uploaded_files,
                    client,
                    edit_media,
                    yt_thumb,
                )
        else:
            sizze = os.path.getsize(local_file_name)
            sent_message = await upload_single_file(
                message,
                local_file_name,
                caption_str,
                from_user,
                client,
                edit_media,
                yt_thumb,
            )
            if sent_message is not None:
                dict_contatining_uploaded_files[
                    os.path.basename(local_file_name)
                ] = sent_message.message_id
            else:
                return
    # await message.delete()
    return dict_contatining_uploaded_files
 
 
# © gautamajay52 thanks to Rclone team for this wonderful tool.🧘
 
 
async def upload_to_gdrive(file_upload, message, messa_ge, g_id):
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    del_it = await message.edit_text(
        f"<a href='tg://user?id={g_id}'>🔊</a> Now Uploading to ☁️ Cloud!!!"
    )
    if not os.path.exists("rclone.conf"):
        with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
            fole.write(f"{RCLONE_CONFIG}")
    if os.path.exists("rclone.conf"):
        with open("rclone.conf", "r+") as file:
            con = file.read()
            gUP = re.findall("\[(.*)\]", con)[0]
            LOGGER.info(gUP)
    destination = f"{DESTINATION_FOLDER}"
    file_upload = str(Path(file_upload).resolve())
    LOGGER.info(file_upload)
    if os.path.isfile(file_upload):
        g_au = [
            "rclone",
            "copy",
            "--config=rclone.conf",
            f"{file_upload}",
            f"{gUP}:{destination}",
            "-v",
        ]
        LOGGER.info(g_au)
        tmp = await asyncio.create_subprocess_exec(
            *g_au, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        gk_file = re.escape(os.path.basename(file_upload))
        LOGGER.info(gk_file)
        with open("filter.txt", "w+", encoding="utf-8") as filter:
            print(f"+ {gk_file}\n- *", file=filter)
 
        t_a_m = [
            "rclone",
            "lsf",
            "--config=rclone.conf",
            "-F",
            "i",
            "--filter-from=filter.txt",
            "--files-only",
            f"{gUP}:{destination}",
        ]
        gau_tam = await asyncio.create_subprocess_exec(
            *t_a_m, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # os.remove("filter.txt")
        gau, tam = await gau_tam.communicate()
        gautam = gau.decode().strip()
        LOGGER.info(gau.decode())
        LOGGER.info(tam.decode())
        # os.remove("filter.txt")
        gauti = f"https://drive.google.com/file/d/{gautam}/view?usp=drivesdk"
        gjay = size(os.path.getsize(file_upload))
        button = []
        button.append(
            [pyrogram.InlineKeyboardButton(text="☁️ CloudUrl ☁️", url=f"{gauti}")]
        )
        if INDEX_LINK:
            indexurl = f"{INDEX_LINK}/{os.path.basename(file_upload)}"
            tam_link = requests.utils.requote_uri(indexurl)
            LOGGER.info(tam_link)
            button.append(
                [
                    pyrogram.InlineKeyboardButton(
                        text="ℹ️ IndexUrl ℹ️", url=f"{tam_link}"
                    )
                ]
            )
        button_markup = pyrogram.InlineKeyboardMarkup(button)
        await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
        await messa_ge.reply_text(
            f"🤖: Uploaded successfully `{os.path.basename(file_upload)}` <a href='tg://user?id={g_id}'>🤒</a>\n📀 Size: {gjay}",
            reply_markup=button_markup,
        )
        os.remove(file_upload)
        await del_it.delete()
    else:
        tt = os.path.join(destination, os.path.basename(file_upload))
        LOGGER.info(tt)
        t_am = [
            "rclone",
            "copy",
            "--config=rclone.conf",
            f"{file_upload}",
            f"{gUP}:{tt}",
            "-v",
        ]
        LOGGER.info(t_am)
        tmp = await asyncio.create_subprocess_exec(
            *t_am, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        pro, cess = await tmp.communicate()
        LOGGER.info(pro.decode("utf-8"))
        LOGGER.info(cess.decode("utf-8"))
        g_file = re.escape(os.path.basename(file_upload))
        LOGGER.info(g_file)
        with open("filter1.txt", "w+", encoding="utf-8") as filter1:
            print(f"+ {g_file}/\n- *", file=filter1)
 
        g_a_u = [
            "rclone",
            "lsf",
            "--config=rclone.conf",
            "-F",
            "i",
            "--filter-from=filter1.txt",
            "--dirs-only",
            f"{gUP}:{destination}",
        ]
        gau_tam = await asyncio.create_subprocess_exec(
            *g_a_u, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # os.remove("filter1.txt")
        gau, tam = await gau_tam.communicate()
        gautam = gau.decode("utf-8")
        LOGGER.info(gautam)
        LOGGER.info(tam.decode("utf-8"))
        # os.remove("filter1.txt")
        gautii = f"https://drive.google.com/folderview?id={gautam}"
        gjay = size(getFolderSize(file_upload))
        LOGGER.info(gjay)
        button = []
        button.append(
            [pyrogram.InlineKeyboardButton(text="☁️ CloudUrl ☁️", url=f"{gautii}")]
        )
        if INDEX_LINK:
            indexurl = f"{INDEX_LINK}/{os.path.basename(file_upload)}/"
            tam_link = requests.utils.requote_uri(indexurl)
            LOGGER.info(tam_link)
            button.append(
                [
                    pyrogram.InlineKeyboardButton(
                        text="ℹ️ IndexUrl ℹ️", url=f"{tam_link}"
                    )
                ]
            )
        button_markup = pyrogram.InlineKeyboardMarkup(button)
        await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
        await messa_ge.reply_text(
            f"🤖: Uploaded successfully `{os.path.basename(file_upload)}` <a href='tg://user?id={g_id}'>🤒</a>\n📀 Size: {gjay}",
            reply_markup=button_markup,
        )
        shutil.rmtree(file_upload)
        await del_it.delete()
 
 
#
 
 
async def upload_single_file(
    message, local_file_name, caption_str, from_user, client, edit_media, yt_thumb
):
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    local_file_name = str(Path(local_file_name).resolve())
    sent_message = None
    start_time = time.time()
    #
    thumbnail_location = os.path.join(
        DOWNLOAD_LOCATION, "thumbnails", str(from_user) + ".jpg"
    )
    # LOGGER.info(thumbnail_location)
    if UPLOAD_AS_DOC.upper() == "TRUE":  # todo
        thumb = None
        thumb_image_path = None
        if os.path.exists(thumbnail_location):
            thumb_image_path = await copy_file(
                thumbnail_location, os.path.dirname(os.path.abspath(local_file_name))
            )
            thumb = thumb_image_path
        message_for_progress_display = message
        if not edit_media:
            message_for_progress_display = await message.reply_text(
                "<b>Trying to upload</b>\n\n📙<b> File Name</b>: <code>{}</code>".format(os.path.basename(local_file_name))
            )
            prog = Progress(from_user, client, message_for_progress_display)
        sent_message = await message.reply_document(
            document=local_file_name,
            thumb=thumb,
            caption=caption_str,
            parse_mode="html",
            disable_notification=True,
            progress=prog.progress_for_pyrogram,
            progress_args=(
                "",
                start_time,
            ),
        )
        if message.message_id != message_for_progress_display.message_id:
            try:
                await message_for_progress_display.delete()
            except FloodWait as gf:
                time.sleep(gf.x)
            except Exception as rr:
                LOGGER.warning(str(rr))
        os.remove(local_file_name)
        if thumb is not None:
            os.remove(thumb)
    else:
        try:
            message_for_progress_display = message
            if not edit_media:
                message_for_progress_display = await message.reply_text(
                    "<b>Trying to upload</b>\n\n📙<b> File Name</b>: <code>{}</code>".format(os.path.basename(local_file_name))
                )
                prog = Progress(from_user, client, message_for_progress_display)
            if local_file_name.upper().endswith(("MKV", "MP4", "WEBM", "M4V", "3GP")):
                duration = 0
                try:
                    metadata = extractMetadata(createParser(local_file_name))
                    if metadata.has("duration"):
                        duration = metadata.get("duration").seconds
                except Exception as g_e:
                    LOGGER.info(g_e)
                width = 0
                height = 0
                thumb_image_path = None
                if os.path.exists(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        os.path.dirname(os.path.abspath(local_file_name)),
                    )
                else:
                    if not yt_thumb:
                        thumb_image_path = await take_screen_shot(
                            local_file_name,
                            os.path.dirname(os.path.abspath(local_file_name)),
                            (duration / 2),
                        )
                    else:
                        req = requests.get(yt_thumb)
                        thumb_image_path = os.path.join(
                            os.path.dirname(os.path.abspath(local_file_name)),
                            str(time.time()) + ".jpg",
                        )
                        with open(thumb_image_path, "wb") as thum:
                            thum.write(req.content)
                        img = Image.open(thumb_image_path).convert("RGB")
                        img.save(thumb_image_path, format="jpeg")
                    # get the correct width, height, and duration for videos greater than 10MB
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                        # ref: https://t.me/PyrogramChat/44663
                        # https://stackoverflow.com/a/21669827/4723940
                        Image.open(thumb_image_path).convert("RGB").save(
                            thumb_image_path
                        )
                        img = Image.open(thumb_image_path)
                        # https://stackoverflow.com/a/37631799/4723940
                        img.resize((320, height))
                        img.save(thumb_image_path, "JPEG")
                        # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
                #
                thumb = None
                if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                    thumb = thumb_image_path
                # send video
                if edit_media and message.photo:
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                    sent_message = await message.edit_media(
                        media=InputMediaVideo(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode="html",
                            width=width,
                            height=height,
                            duration=duration,
                            supports_streaming=True,
                        )
                        # quote=True,
                    )
                else:
                    sent_message = await message.reply_video(
                        video=local_file_name,
                        caption=caption_str,
                        parse_mode="html",
                        duration=duration,
                        width=width,
                        height=height,
                        thumb=thumb,
                        supports_streaming=True,
                        disable_notification=True,
                        progress=prog.progress_for_pyrogram,
                        progress_args=(
                            "",
                            start_time,
                        ),
                    )
                if thumb is not None:
                    os.remove(thumb)
            elif local_file_name.upper().endswith(("MP3", "M4A", "M4B", "FLAC", "WAV")):
                metadata = extractMetadata(createParser(local_file_name))
                duration = 0
                title = ""
                artist = ""
                if metadata.has("duration"):
                    duration = metadata.get("duration").seconds
                if metadata.has("title"):
                    title = metadata.get("title")
                if metadata.has("artist"):
                    artist = metadata.get("artist")
                thumb_image_path = None
                if os.path.isfile(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        os.path.dirname(os.path.abspath(local_file_name)),
                    )
                thumb = None
                if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                    thumb = thumb_image_path
                # send audio
                if edit_media and message.photo:
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                    sent_message = await message.edit_media(
                        media=InputMediaAudio(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode="html",
                            duration=duration,
                            performer=artist,
                            title=title,
                        )
                    )
                else:
                    sent_message = await message.reply_audio(
                        audio=local_file_name,
                        caption=caption_str,
                        parse_mode="html",
                        duration=duration,
                        performer=artist,
                        title=title,
                        thumb=thumb,
                        disable_notification=True,
                        progress=prog.progress_for_pyrogram,
                        progress_args=(
                            "",
                            start_time,
                        ),
                    )
                if thumb is not None:
                    os.remove(thumb)
            else:
                thumb_image_path = None
                if os.path.isfile(thumbnail_location):
                    thumb_image_path = await copy_file(
                        thumbnail_location,
                        os.path.dirname(os.path.abspath(local_file_name)),
                    )
                # if a file, don't upload "thumb"
                # this "diff" is a major derp -_- 😔😭😭
                thumb = None
                if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                    thumb = thumb_image_path
                #
                # send document
                if edit_media and message.photo:
                    sent_message = await message.edit_media(
                        media=InputMediaDocument(
                            media=local_file_name,
                            thumb=thumb,
                            caption=caption_str,
                            parse_mode="html",
                        )
                    )
                else:
                    sent_message = await message.reply_document(
                        document=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        disable_notification=True,
                        progress=prog.progress_for_pyrogram,
                        progress_args=(
                            "",
                            start_time,
                        ),
                    )
                if thumb is not None:
                    os.remove(thumb)
 
        except MessageNotModified as oY:
            LOGGER.info(oY)
        except FloodWait as g:
            LOGGER.info(g)
            time.sleep(g.x)
        except Exception as e:
            LOGGER.info(e)
            await message_for_progress_display.edit_text("**FAILED**\n" + str(e))
        else:
            if message.message_id != message_for_progress_display.message_id:
                try:
                    if sent_message is not None:
                        await message_for_progress_display.delete()
                except FloodWait as gf:
                    time.sleep(gf.x)
                except Exception as rr:
                    LOGGER.warning(str(rr))
                    await asyncio.sleep(5)
        os.remove(local_file_name)
    return sent_message
