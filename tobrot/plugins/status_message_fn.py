#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

import asyncio
import io
import logging
import os
import shutil
import sys
import time
import traceback

import psutil
import math
from pyrogram.errors import FloodWait, MessageIdInvalid, MessageNotModified
from tobrot.helper_funcs.admin_check import AdminCheck

from tobrot import (
    AUTH_CHANNEL,
    BOT_START_TIME,
    LOGGER,
    MAX_MESSAGE_LENGTH, 
    user_specific_config,
    gid_dict,
    _lock,
    EDIT_SLEEP_TIME_OUT,
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR
    )


# the logging things
from tobrot.helper_funcs.display_progress import TimeFormatter, humanbytes
from tobrot.helper_funcs.download_aria_p_n import (aria_start,
                                                   call_apropriate_function)
from tobrot.helper_funcs.upload_to_tg import upload_to_tg
from tobrot.UserDynaConfig import UserDynaConfig


async def upload_as_doc(client, message):
    user_specific_config[message.from_user.id]=UserDynaConfig(message.from_user.id,True)
    await message.reply_text("**🗞 Your Files Will Be Uploaded As Document 📁**")


async def upload_as_video(client, message):
    user_specific_config[message.from_user.id]=UserDynaConfig(message.from_user.id,False)
    await message.reply_text("**🗞 Your Files Will Be Uploaded As Streamable 🎞**")
 

async def status_message_f(
    client, message
):  # weird code but 'This is the way' @gautamajay52
    aria_i_p = await aria_start()
    # Show All Downloads
    to_edit = await message.reply(".......")
    chat_id = int(message.chat.id)
    mess_id = int(to_edit.message_id)
    async with _lock:
        if len(gid_dict[chat_id]) == 0:
            gid_dict[chat_id].append(mess_id)
        else:
            if not mess_id in gid_dict[chat_id]:
                await client.delete_messages(chat_id, gid_dict[chat_id])
                gid_dict[chat_id].pop()
                gid_dict[chat_id].append(mess_id)

    prev_mess = "By gautamajay52"
    await message.delete()
    while True:
        downloads = aria_i_p.get_downloads()
        msg = ""
        for file in downloads:
            downloading_dir_name = "NA"
            try:
                downloading_dir_name = str(file.name)
            except:
                pass
            if file.status == "active":
                is_file = file.seeder
                if is_file is None:
                    msgg = f"<b>Conn:</b> {file.connections}"
                else:
                    msgg = f"<b>Peers:</b> {file.connections} | <b>Seeders:</b> {file.num_seeders}"

                percentage = int(file.progress_string(0).split('%')[0])
                prog = "[{0}{1}]".format("".join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 5))]),"".join([UN_FINISHED_PROGRESS_STR for i in range(20 - math.floor(percentage / 5))]))
                msg += f"<b>════════════════════════════════</b>\n"
                msg += f"\n<b>{downloading_dir_name}</b>"
                msg += f"\n<b>{prog}</b>"
                msg += f"\n<b>Speed</b>: {file.download_speed_string()}"
                msg += f"\n<b>Status</b>: {file.progress_string()} <b>of</b> {file.total_length_string()}"
                msg += f"\n<b>ETA:</b> {file.eta_string()}"
                msg += f"\n{msgg}"
                msg += f"\n<b>To Cancel:</b> <code>/cancel {file.gid}</code>"
                msg += "\n"

        hr, mi, se = up_time(time.time() - BOT_START_TIME)
        total, used, free = shutil.disk_usage(".")
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)

        ms_g = (
            f"<b>Bot Uptime</b>: <code>{hr} : {mi} : {se}</code>\n"
            f"<b>T:</b> <code>{total}</code> <b>U:</b> <code>{used}</code> <b>F:</b> <code>{free}</code>\n"
            f"<b>RAM:</b> <code>{ram}%</code> <b>CPU:</b> <code>{cpu}%</code>\n"
        )
        if msg == "":
            msg = "🤷‍♂️ No Active, Queued or Paused TORRENTs"
            msg = ms_g + "\n" + msg
            await to_edit.edit(msg)
            break
        msg = msg + "\n" + ms_g
        if len(msg) > MAX_MESSAGE_LENGTH:  # todo - will catch later
            with io.BytesIO(str.encode(msg)) as out_file:
                out_file.name = "status.text"
                await client.send_document(
                    chat_id=message.chat.id,
                    document=out_file,
                )
            break
        else:
            if msg != prev_mess:
                try:
                    await to_edit.edit(msg, parse_mode="html")
                except MessageIdInvalid as df:
                    break
                except MessageNotModified as ep:
                    LOGGER.info(ep)
                    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                except FloodWait as e:
                    LOGGER.info(e)
                    time.sleep(e.x)
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                prev_mess = msg


async def cancel_message_f(client, message):
    if len(message.command) > 1:
        # /cancel command
        i_m_s_e_g = await message.reply_text("checking..?", quote=True)
        aria_i_p = await aria_start()
        g_id = message.command[1].strip()
        LOGGER.info(g_id)
        try:
            downloads = aria_i_p.get_download(g_id)
            name = downloads.name
            size = downloads.total_length_string()
            gid_list = downloads.followed_by_ids
            downloads = [downloads]
            if len(gid_list) != 0:
                downloads = aria_i_p.get_downloads(gid_list)
            aria_i_p.remove(downloads=downloads, force=True, files=True, clean=True)
            await i_m_s_e_g.edit_text(
                f"Download cancelled :\n<code>{name} ({size})</code> by <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>"
            )
        except Exception as e:
            await i_m_s_e_g.edit_text("<i>FAILED</i>\n\n" + str(e) + "\n#error")
    else:
        await message.delete()


async def exec_message_f(client, message):
    if message.from_user.id in AUTH_CHANNEL:
        DELAY_BETWEEN_EDITS = 0.3
        PROCESS_RUN_TIME = 100
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.message_id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.message_id

        start_time = time.time() + PROCESS_RUN_TIME
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "No Error"
        o = stdout.decode()
        if not o:
            o = "No Output"
        else:
            _o = o.split("\n")
            o = "`\n".join(_o)
        OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

        if len(OUTPUT) > MAX_MESSAGE_LENGTH:
            with io.BytesIO(str.encode(OUTPUT)) as out_file:
                out_file.name = "exec.text"
                await client.send_document(
                    chat_id=message.chat.id,
                    document=out_file,
                    caption=cmd,
                    disable_notification=True,
                    reply_to_message_id=reply_to_id,
                )
            await message.delete()
        else:
            await message.reply_text(OUTPUT)


async def upload_document_f(client, message):
    imsegd = await message.reply_text("processing ...")
    if message.from_user.id in AUTH_CHANNEL:
        if " " in message.text:
            recvd_command, local_file_name = message.text.split(" ", 1)
            recvd_response = await upload_to_tg(
                imsegd, local_file_name, message.from_user.id, {}, client
            )
            LOGGER.info(recvd_response)
    await imsegd.delete()


async def eval_message_f(client, message):
    if message.from_user.id in AUTH_CHANNEL:
        status_message = await message.reply_text("Processing ...")
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.message_id
        if message.reply_to_message:
            reply_to_id = message.reply_to_message.message_id

        old_stderr = sys.stderr
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()
        redirected_error = sys.stderr = io.StringIO()
        stdout, stderr, exc = None, None, None

        try:
            await aexec(cmd, client, message)
        except Exception:
            exc = traceback.format_exc()

        stdout = redirected_output.getvalue()
        stderr = redirected_error.getvalue()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        evaluation = ""
        if exc:
            evaluation = exc
        elif stderr:
            evaluation = stderr
        elif stdout:
            evaluation = stdout
        else:
            evaluation = "Success"

        final_output = (
            "<b>EVAL</b>: <code>{}</code>\n\n<b>OUTPUT</b>:\n<code>{}</code> \n".format(
                cmd, evaluation.strip()
            )
        )

        if len(final_output) > MAX_MESSAGE_LENGTH:
            with open("eval.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(final_output))
            await message.reply_document(
                document="eval.text",
                caption=cmd,
                disable_notification=True,
                reply_to_message_id=reply_to_id,
            )
            os.remove("eval.text")
            await status_message.delete()
        else:
            await status_message.edit(final_output)


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


def up_time(time_taken):
    hours, _hour = divmod(time_taken, 3600)
    minutes, seconds = divmod(_hour, 60)
    return round(hours), round(minutes), round(seconds)


async def upload_log_file(client, message):
    g = await AdminCheck(client, message.chat.id, message.from_user.id)
    if g:
        await message.reply_document("Torrentleech-Gdrive.txt")