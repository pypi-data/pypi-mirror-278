#!/usr/bin/env python

"""
 * laravel-ignition-Rxss
 * laravel-ignition-Rxss Bug scanner for WebPentesters and Bugbounty Hunters
 *
 * @Developed By Cappricio Securities <https://cappriciosec.com>
 */


"""
import getpass
username = getpass.getuser()


def display_help():
    help_banner = f"""

👋 Hey \033[96m{username}
   \033[92m                                                                                                v1.0
    __                            __      _             _ __  _                   ____
   / /___ __________ __   _____  / /     (_)___ _____  (_) /_(_)___  ____        / __ \_  ____________
  / / __ `/ ___/ __ `/ | / / _ \/ /_____/ / __ `/ __ \/ / __/ / __ \/ __ \______/ /_/ / |/_/ ___/ ___/
 / / /_/ / /  / /_/ /| |/ /  __/ /_____/ / /_/ / / / / / /_/ / /_/ / / / /_____/ _, _/>  <(__  |__  )
/_/\__,_/_/   \__,_/ |___/\___/_/     /_/\__, /_/ /_/_/\__/_/\____/_/ /_/     /_/ |_/_/|_/____/____/
                                        /____/
                                                            \033[0mDeveloped By \x1b[31;1m\033[4mhttps://cappriciosec.com\033[0m


\x1b[31;1mlaravel-ignition-Rxss : Bug scanner for WebPentesters and Bugbounty Hunters

\x1b[31;1m$ \033[92mlaravel-ignition-Rxss\033[0m [option]

Usage: \033[92mlaravel-ignition-Rxss\033[0m [options]

Options:
  -u, --url     URL to scan                                laravel-ignition-Rxss -u https://target.com
  -i, --input   <filename> Read input from txt             laravel-ignition-Rxss -i target.txt
  -o, --output  <filename> Write output in txt file        laravel-ignition-Rxss -i target.txt -o output.txt
  -c, --chatid  Creating Telegram Notification             laravel-ignition-Rxss --chatid yourid
  -b, --blog    To Read about laravel-ignition-Rxss Bug    laravel-ignition-Rxss -b
  -h, --help    Help Menu
    """
    print(help_banner)


def banner():
    help_banner = f"""
    \033[94m
👋 Hey \033[96m{username}
      \033[92m                                                                                             v1.0
    __                            __      _             _ __  _                   ____
   / /___ __________ __   _____  / /     (_)___ _____  (_) /_(_)___  ____        / __ \_  ____________
  / / __ `/ ___/ __ `/ | / / _ \/ /_____/ / __ `/ __ \/ / __/ / __ \/ __ \______/ /_/ / |/_/ ___/ ___/
 / / /_/ / /  / /_/ /| |/ /  __/ /_____/ / /_/ / / / / / /_/ / /_/ / / / /_____/ _, _/>  <(__  |__  )
/_/\__,_/_/   \__,_/ |___/\___/_/     /_/\__, /_/ /_/_/\__/_/\____/_/ /_/     /_/ |_/_/|_/____/____/
                                        /____/
                                                                  \033[0mDeveloped By \x1b[31;1m\033[4mhttps://cappriciosec.com\033[0m


\x1b[31;1mlaravel-ignition-Rxss : Bug scanner for WebPentesters and Bugbounty Hunters

\033[0m"""
    print(help_banner)
