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


import asyncio
import os
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config


async def split_large_files(input_file):
    working_directory = os.path.dirname(os.path.abspath(input_file))
    new_working_directory = os.path.join(
        working_directory,
        str(time.time())
    )
    # create download directory, if not exist
    if not os.path.isdir(new_working_directory):
        os.makedirs(new_working_directory)
    if input_file.upper().endswith(("MKV", "MP4", "WEBM", "MP3", "M4A", "FLAC", "WAV")):
    # if False:
        # handle video / audio files here
        metadata = extractMetadata(createParser(input_file))
        total_duration = 0
        if metadata.has("duration"):
            total_duration = metadata.get('duration').seconds
        # proprietary logic to get the seconds to trim (at)
        LOGGER.info(total_duration)
        total_file_size = os.path.getsize(input_file)
        LOGGER.info(total_file_size)
        minimum_duration = (total_duration / total_file_size) * (Config.MAX_TG_SPLIT_FILE_SIZE)
        LOGGER.info(minimum_duration)
        # END: proprietary
        start_time = 0
        end_time = minimum_duration
        base_name = os.path.basename(input_file)
        input_extension = base_name.split(".")[-1]
        LOGGER.info(input_extension)
        i = 0
        while end_time < total_duration:
            LOGGER.info(i)
            parted_file_name = "" + str(i) + str(base_name) + "_PART_" + str(start_time) + "." + str(input_extension)
            output_file = os.path.join(new_working_directory, parted_file_name)
            LOGGER.info(output_file)
            LOGGER.info(await cult_small_video(
                input_file,
                output_file,
                str(start_time),
                str(end_time)
            ))
            start_time = end_time
            end_time = end_time + minimum_duration
            i = i + 1
    else:
        # handle normal files here
        o_d_t = os.path.join(
            new_working_directory,
            os.path.basename(input_file)
        )
        o_d_t = o_d_t + "."
        file_genertor_command = [
            "split",
            "-d",
            "--suffix-length=5",
            "--bytes=1572863000",
            input_file,
            o_d_t
        ]
        process = await asyncio.create_subprocess_exec(
            *file_genertor_command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
    return new_working_directory


async def cult_small_video(video_file, out_put_file_name, start_time, end_time):
    file_genertor_command = [
        "ffmpeg",
        "-hide_banner",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        "-c",
        "copy",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    LOGGER.info(t_response)
    return out_put_file_name
