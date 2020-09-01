#!/usr/bin/env python3
# -*- coding: utf-8 -*-


async def AdminCheck(client, chat_id, user_id):
    SELF = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "creator",
        "administrator"
    ]
    # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
    if SELF.status not in admin_strings:
        return False
    else:
        return True
