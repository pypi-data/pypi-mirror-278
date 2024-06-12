
<div align="center">
  <img src="https://blogs.cappriciosec.com/uploaders/Laravel-Ignition-Rxss-tool.png" alt="logo">
</div>


## Badges



[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![PyPI - Version](https://img.shields.io/pypi/v/laravel-ignition-rxss)
![PyPI - Downloads](https://img.shields.io/pypi/dm/laravel-ignition-rxss)
![GitHub all releases](https://img.shields.io/github/downloads/Cappricio-Securities/laravel-ignition-rxss/total)
<a href="https://github.com/Cappricio-Securities/laravel-ignition-rxss/releases/"><img src="https://img.shields.io/github/release/Cappricio-Securities/laravel-ignition-rxss"></a>![Profile_view](https://komarev.com/ghpvc/?username=Cappricio-Securities&label=Profile%20views&color=0e75b6&style=flat)
[![Follow Twitter](https://img.shields.io/twitter/follow/cappricio_sec?style=social)](https://twitter.com/cappricio_sec)
<p align="center">

<p align="center">







## License

[MIT](https://choosealicense.com/licenses/mit/)



## Installation 

1. Install Python3 and pip [Instructions Here](https://www.python.org/downloads/) (If you can't figure this out, you shouldn't really be using this)

   - Install via pip
     - ```bash
          pip install laravel-ignition-rxss 
        ```
   - Run bellow command to check
     - `laravel-ignition-rxss -h`

## Configurations 
2. We integrated with the Telegram API to receive instant notifications for vulnerability detection.
   
   - Telegram Notification
     - ```bash
          laravel-ignition-rxss --chatid <YourTelegramChatID>
        ```
   - Open your telegram and search for [`@CappricioSecuritiesTools_bot`](https://web.telegram.org/k/#@CappricioSecuritiesTools_bot) and click start

## Usages 
3. This tool has multiple use cases.
   
   - To Check Single URL
     - ```bash
          laravel-ignition-rxss -u http://example.com 
        ```
   - To Check List of URL 
      - ```bash
          laravel-ignition-rxss -i urls.txt 
        ```
   - Save output into TXT file
      - ```bash
          laravel-ignition-rxss -i urls.txt -o out.txt
        ```
   - Want to Learn about [`laravel-ignition-rxss`](https://blogs.cappriciosec.com/cve/162/Laravel%20Ignition's%20XSS%20Vulnerability)? Then Type Below command
      - ```bash
          laravel-ignition-rxss -b
        ```
     
<p align="center">
  <b>🚨 Disclaimer</b>
  
</p>
<p align="center">
<b>This tool is created for security bug identification and assistance; Cappricio Securities is not liable for any illegal use. 
  Use responsibly within legal and ethical boundaries. 🔐🛡️</b></p>


## Working PoC Video

[![asciicast](https://blogs.cappriciosec.com/uploaders/Screenshot%202024-05-29%20at%2010.45.10%20AM.png)](https://asciinema.org/a/rp52UB23dZv3JGkd9zBnhhTB9)




## Help menu

#### Get all items

```bash
👋 Hey Hacker
                                                                                                   v1.0
    __                            __      _             _ __  _                   ____
   / /___ __________ __   _____  / /     (_)___ _____  (_) /_(_)___  ____        / __ \_  ____________
  / / __ `/ ___/ __ `/ | / / _ \/ /_____/ / __ `/ __ \/ / __/ / __ \/ __ \______/ /_/ / |/_/ ___/ ___/
 / / /_/ / /  / /_/ /| |/ /  __/ /_____/ / /_/ / / / / / /_/ / /_/ / / / /_____/ _, _/>  <(__  |__  )
/_/\__,_/_/   \__,_/ |___/\___/_/     /_/\__, /_/ /_/_/\__/_/\____/_/ /_/     /_/ |_/_/|_/____/____/
                                        /____/
                                                            Developed By https://cappriciosec.com
                              

laravel-ignition-rxss : Bug scanner for WebPentesters and Bugbounty Hunters 

$ laravel-ignition-rxss [option]

Usage: laravel-ignition-rxss [options]
```


| Argument | Type     | Description                | Examples |
| :-------- | :------- | :------------------------- | :------------------------- |
| `-u` | `--url` | URL to scan | laravel-ignition-rxss -u https://target.com |
| `-i` | `--input` | filename Read input from txt  | laravel-ignition-rxss -i target.txt | 
| `-o` | `--output` | filename Write output in txt file | laravel-ignition-rxss -i target.txt -o output.txt |
| `-c` | `--chatid` | Creating Telegram Notification | laravel-ignition-rxss --chatid yourid |
| `-b` | `--blog` | To Read about laravel-ignition-rxss Bug | laravel-ignition-rxss -b |
| `-h` | `--help` | Help Menu | laravel-ignition-rxss -h |



## 🔗 Links
[![Website](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://cappriciosec.com/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/karthikeyan--v/)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/karthithehacker)



## Author

- [@karthithehacker](https://github.com/karthi-the-hacker/)



## Feedback

If you have any feedback, please reach out to us at contact@karthithehacker.com
