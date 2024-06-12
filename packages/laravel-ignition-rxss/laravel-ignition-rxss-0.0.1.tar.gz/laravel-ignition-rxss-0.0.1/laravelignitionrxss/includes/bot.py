#!/usr/bin/env python

"""
 * laravel-ignition-Rxss
 * laravel-ignition-Rxss Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */
"""
import requests
from laravelignitionrxss.utils import const
from laravelignitionrxss.utils import configure


def sendmessage(vul):

    data = {"Tname": "laravel-ignition-Rxss", "chatid": configure.get_chatid(), "data": vul,
            "Blog": const.Data.blog, "bugname": const.Data.bugname, "Priority": "Medium"}

    headers = {
        "Content-Type": "application/json",
    }

    try:
        response = requests.put(const.Data.api, json=data, headers=headers)
    except:
        print("Bot Error")
