# Microsoft-Rewards-Bot

Microsoft Rewards (Bing Rewards) Bot - Completes searches and quizzes, written in Python! :raised_hands:

## Overview

This program will automatically complete search requests and quizzes on Microsoft Rewards! Search terms are the daily top searches retrieved using Google Trends' API. This bot runs selenium in headless mode for deployment on VPS and for increased performance on local machines. The bot also uses selenium's user agent options to fulfill points for all three platforms (pc, edge browser, mobile). 100% free to use and open source. Code critique/feedback and contributions welcome!

## Features

- Completes PC search, Edge search, Mobile search via user agents
- Retrieves top daily searches via Google Trends' API
- Completes polls, all types of quizzes (multiple choice, click and drag and reorder), punch cards and explore dailies
- Headless mode (Confirmed working on DigitalOcean linux droplet)
- Supports unlimited accounts via JSON.
- Randomized search speeds
- Logs errors and info by default, can log executed commands and search terms by changing the log level to DEBUG
- Tested and confirmed working for U.K. (more to come!)

## Requirements

- Python          [3.9](https://www.python.org/downloads/)
- Requests        2.25.1
- Selenium        3.141.0
- pyotp           2.6.0
- Chrome Browser  (Up-to-date)

## How to Use

1.  Clone and navigate to repo or download the latest [release](https://github.com/tmxkn1/Microsoft-Rewards-Bot/releases).
2.  Modify `ms_rewards_login_dict.json.example` with your account names and passwords,
    remove `.example` from filename.
3.  If your account has 2-factor authentication (2FA) enabled, please follow [README-2FA](README-2FA.md).
4.  Enter into cmd/terminal/shell: `python -m pip install -r requirements.txt`
    - This installs dependencies (selenium, requests and pytop)
5.  Enter into cmd/terminal/shell: `python ms_rewards.py --headless --mobile --pc --quiz`
    - enter `-h` or `--help` for more instructions
    - `--headless` is for headless mode
    - `--mobile` is for mobile search
    - `--pc` is for pc search
    - `--quiz` is for quiz search
    - `-a` or `--all` is short for mobile, pc, and quiz search
    - Script by default will execute mobile, pc, edge, searches, and complete quizzes for all accounts (can change this setting in the .py file)
    - Script by default will run in interactive mode
    - If python environment variable is not set, enter `/path/to/python/executable ms_rewards.py`
6.  Crontab (Optional for automated script daily on linux)
    - Enter in terminal: `crontab -e`
    - Enter in terminal: `0 12 * * * /path/to/python /path/to/ms_rewards.py --headless --mobile --pc --quiz`
      - Can change the time from 12am server time to whenever the MS daily searches reset (~12am PST)
      - Change the paths to the json in the .py file to appropriate path

## To Do

- High priority:
  - More logging
  - More type hint
  - Windows notification
- Low priority:
  - Proxy support
  - Multithreaded mode or seleniumGrid
  - Support for other regions
  - Telegram Intergration for reporting bot status/total points.

## License

100% free to use and open source. :see_no_evil: :hear_no_evil: :speak_no_evil:

## Versions

For a summary of changes in each version of the bot, please see
**[CHANGELOG](CHANGELOG.md).**

#### Credit

@LjMario007 - for previous developments<br />
@blackluv - for the original idea and developments<br />
@ShoGinn - for extraordinary assistance in making this project better!
