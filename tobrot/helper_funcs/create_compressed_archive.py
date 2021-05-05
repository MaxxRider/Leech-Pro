#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

import asyncio
import logging
import os
import shutil
import subprocess

from tobrot import LOGGER


async def create_archive(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        compressed_file_name = f"{base_dir_name}.tar.gz"
        # #BlameTelegram
        suffix_extention_length = 1 + 3 + 1 + 2
        if len(base_dir_name) > (64 - suffix_extention_length):
            compressed_file_name = base_dir_name[0 : (64 - suffix_extention_length)]
            compressed_file_name += ".tar.gz"
        # fix for https://t.me/c/1434259219/13344
        file_genertor_command = [
            "tar",
            "-zcvf",
            compressed_file_name,
            f"{input_directory}",
        ]
        process = await asyncio.create_subprocess_exec(
            *file_genertor_command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()
        LOGGER.error(stderr.decode().strip())
        if os.path.exists(compressed_file_name):
            try:
                shutil.rmtree(input_directory)
            except:
                pass
            return_name = compressed_file_name
    return return_name


# @gautamajay52


async def unzip_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        # uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        uncompressed_file_name = get_base_name(base_dir_name)
        LOGGER.info(uncompressed_file_name)
        g_cmd = ["./extract", f"{input_directory}"]
        ga_utam = await asyncio.create_subprocess_exec(
            *g_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # Wait for the subprocess to finish
        gau, tam = await ga_utam.communicate()
        LOGGER.info(gau.decode().strip())
        LOGGER.info(tam.decode().strip())
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
    return return_name


#


async def untar_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        print(input_directory)
        base_dir_name = os.path.basename(input_directory)
        uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        m_k_gaut = ["mkdir", f"{uncompressed_file_name}"]
        await asyncio.create_subprocess_exec(
            *m_k_gaut, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        g_cmd_t = [
            "tar",
            "-xvf",
            f"/app/{base_dir_name}",
            "-C",
            f"{uncompressed_file_name}",
        ]
        bc_kanger = await asyncio.create_subprocess_exec(
            *g_cmd_t, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # Wait for the subprocess to finish
        mc, kanger = await bc_kanger.communicate()
        LOGGER.info(mc)
        LOGGER.info(kanger)
        # e_response = stderr.decode().strip()
        # t_response = stdout.decode().strip()
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
            LOGGER.info(return_name)
    return return_name


#


async def unrar_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        m_k_gau = ["mkdir", f"{uncompressed_file_name}"]
        await asyncio.create_subprocess_exec(
            *m_k_gau, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        print(base_dir_name)
        gau_tam_r = ["unrar", "x", f"{base_dir_name}", f"{uncompressed_file_name}"]
        jai_hind = await asyncio.create_subprocess_exec(
            *gau_tam_r, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        # Wait for the subprocess to finish
        jai, hind = await jai_hind.communicate()
        LOGGER.info(jai)
        LOGGER.info(hind)
        # e_response = stderr.decode().strip()
        # t_response = stdout.decode().strip()
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
            LOGGER.info(return_name)
    return return_name


def get_base_name(orig_path: str):
    if orig_path.endswith(".tar.bz2"):
        return orig_path.replace(".tar.bz2", "")
    elif orig_path.endswith(".tar.gz"):
        return orig_path.replace(".tar.gz", "")
    elif orig_path.endswith(".bz2"):
        return orig_path.replace(".bz2", "")
    elif orig_path.endswith(".gz"):
        return orig_path.replace(".gz", "")
    elif orig_path.endswith(".tar"):
        return orig_path.replace(".tar", "")
    elif orig_path.endswith(".tbz2"):
        return orig_path.replace("tbz2", "")
    elif orig_path.endswith(".tgz"):
        return orig_path.replace(".tgz", "")
    elif orig_path.endswith(".zip"):
        return orig_path.replace(".zip", "")
    elif orig_path.endswith(".7z"):
        return orig_path.replace(".7z", "")
    elif orig_path.endswith(".Z"):
        return orig_path.replace(".Z", "")
    elif orig_path.endswith(".rar"):
        return orig_path.replace(".rar", "")
    else:
        raise Exception("File format not supported for extraction")
