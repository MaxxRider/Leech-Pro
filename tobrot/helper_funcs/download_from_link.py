#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | MaxxRider

import asyncio
import logging
import os
import time

from tobrot import DOWNLOAD_LOCATION, LOGGER


async def request_download(url, file_name, r_user_id):
    directory_path = os.path.join(DOWNLOAD_LOCATION, str(r_user_id), str(time.time()))
    # create download directory, if not exist
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)
    local_file_path = os.path.join(directory_path, file_name)
    command_to_exec = ["wget", "-O", local_file_path, url]
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    # logger.info(e_response)
    t_response = stdout.decode().strip()
    # logger.info(t_response)
    final_m_r = e_response + "\n\n\n" + t_response
    if os.path.exists(local_file_path):
        return True, local_file_path
    else:
        return False, final_m_r
