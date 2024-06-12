#!/usr/bin/env python

"""
 * laravel-ignition-Rxss
 * laravel-ignition-Rxss Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */


"""


class Data:
    blog = 'https://blogs.cappriciosec.com/cve/162/Laravel%20Ignition'
    api = 'https://api.cappriciosec.com/Telegram/cappriciosecbot.php'
    config_path = '~/.config/cappriciosec-tools/cappriciosec.yaml'
    payloadurl = 'https://raw.githubusercontent.com/Cappricio-Securities/PayloadAllTheThings/main/laravel-ignition-Rxss.txt'
    bugname = 'Laravel Ignition - Reflected Cross-Site Scripting'
    rheaders = {
        "User-Agent": "cappriciosec.com",
        "Tool-Name": "laravel-ignition-Rxss",
        "Developed-by": "cappriciosec.com",
        "Contact-us": "contact@cappriciosec.com"
    }


class Colors:
    RED = '\x1b[31;1m'
    BLUE = '\x1b[34;1m'
    GREEN = '\x1b[32;1m'
    RESET = '\x1b[0m'
    MAGENTA = '\x1b[35;1m'
