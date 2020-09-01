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


from shutil import copyfile
import os
import time


async def copy_file(input_file, output_dir):
    output_file = os.path.join(
        output_dir,
        str(time.time()) + ".jpg"
    )
    # https://stackoverflow.com/a/123212/4723940
    copyfile(input_file, output_file)
    return output_file
