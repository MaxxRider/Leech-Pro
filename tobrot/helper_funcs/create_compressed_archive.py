#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
LOGGER = logging.getLogger(__name__)

import asyncio
import os
import shutil
import subprocess


async def create_archive(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        compressed_file_name = f"{base_dir_name}.tar.gz"
        # #BlameTelegram
        suffix_extention_length = 1 + 3 + 1 + 2
        if len(base_dir_name) > (64 - suffix_extention_length):
            compressed_file_name = base_dir_name[0:(64 - suffix_extention_length)]
            compressed_file_name += ".tar.gz"
        # fix for https://t.me/c/1434259219/13344
        file_genertor_command = [
            "tar",
            "-zcvf",
            compressed_file_name,
            f"{input_directory}"
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
        if os.path.exists(compressed_file_name):
            try:
                shutil.rmtree(input_directory)
            except:
                pass
            return_name = compressed_file_name
    return return_name

#@gautamajay52

async def unzip_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        # #BlameTelegram
        #suffix_extention_length = 1 + 3 + 1 + 2
        #if len(base_dir_name) > (64 - suffix_extention_length):
            #compressed_file_name = base_dir_name[0:(64 - suffix_extention_length)]
            #compressed_file_name += ".tar.gz"
        # fix for https://t.me/c/1434259219/13344
        g_cmd = ["unzip", "-o", f"{base_dir_name}", "-d", f"{uncompressed_file_name}"]
        ga_utam = await asyncio.create_subprocess_exec(*g_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        # Wait for the subprocess to finish
        gau, tam = await ga_utam.communicate()
        print(gau)
        print(tam)
        #e_response = stderr.decode().strip()
        #t_response = stdout.decode().strip()
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
            print(return_name)
    return return_name
#
async def untar_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        print(input_directory)
        base_dir_name = os.path.basename(input_directory)
        uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        m_k_gaut = ['mkdir', f'{uncompressed_file_name}']
        await asyncio.create_subprocess_exec(*m_k_gaut, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        g_cmd_t = ["tar", "-xvf", f"/app/{base_dir_name}", "-C", f"{uncompressed_file_name}"]
        bc_kanger = await asyncio.create_subprocess_exec(*g_cmd_t, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        # Wait for the subprocess to finish
        mc, kanger = await bc_kanger.communicate()
        print(mc)
        print(kanger)
        #e_response = stderr.decode().strip()
        #t_response = stdout.decode().strip()
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
            print(return_name)
    return return_name
#
async def unrar_me(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        uncompressed_file_name = os.path.splitext(base_dir_name)[0]
        m_k_gau = ['mkdir', f'{uncompressed_file_name}']
        await asyncio.create_subprocess_exec(*m_k_gau, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        print(base_dir_name)
        gau_tam_r = ["unrar", "x", f"{base_dir_name}", f"{uncompressed_file_name}"]
        jai_hind = await asyncio.create_subprocess_exec(*gau_tam_r, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        # Wait for the subprocess to finish
        jai, hind = await jai_hind.communicate()
        print(jai)
        print(hind)
        #e_response = stderr.decode().strip()
        #t_response = stdout.decode().strip()
        if os.path.exists(uncompressed_file_name):
            try:
                os.remove(input_directory)
            except:
                pass
            return_name = uncompressed_file_name
            print(return_name)
    return return_name
