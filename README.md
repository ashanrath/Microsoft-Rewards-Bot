# Microsoft-Rewards-Bot

Microsoft Rewards (Bing Rewards) Bot - Completes searches and quizzes, written in Python! :raised_hands:

## Overview

This program will automatically complete search requests and quizzes on Microsoft Rewards! Search terms are the daily top searches retrieved using Google Trends' API. This bot runs selenium in headless mode for deployment on VPS and for increased performance on local machines. The bot also uses selenium's user agent options to fulfill points for all three platforms (pc, edge browser, mobile). 100% free to use and open source. Code critique/feedback and contributions welcome!

## Features
- Completes PC search, Edge search and Mobile search
- Completes polls, all types of quizzes (multiple choice, click and drag and reorder), punch cards and explore dailies
- Retrieves top daily searches via Google Trends' API
- Headless mode
- Supports unlimited accounts via JSON.
- Randomized search speeds
- Logs errors and info by default, can log executed commands and search terms by changing the log level to DEBUG

## Requirements
- Python          		[3.9](https://www.python.org/downloads/)
- Requests        		2.27.1
- Selenium        		4.0.0b4
- pyotp           		2.6.0
- python-telegram-bot	13.7
- Chrome Browser  		(Up-to-date)

## Use

1.  Clone and navigate to repo (recommended) or download the latest [release](https://github.com/tmxkn1/Microsoft-Rewards-Bot/releases).
2.  Modify `options/login_cred.json.example` with your account names and passwords,
    remove `.example` from filename.
3.  If your account has 2-factor authentication (2FA) enabled, please follow [README-2FA](READMEs/README-2FA.md).
4.  Enter into cmd/terminal/shell: `python -m pip install -r requirements.txt`
5.  Enter into cmd/terminal/shell: `python ms_rewards.py --headless --mobile --pc --quiz`.
    - enter `-h` or `--help` for more instructions
    - `--telegram` is to enable telegram integration. Please follow please follow [README-Telegram](READMEs/README-Telegram.md).

*Hint: Replace `ms_rewards.py` with `ms_rewards.quiet.pyw` to run the bot in the background without a command window.*
### Optional
- Crontab (automated script daily on linux)
    - Enter in terminal: `crontab -e`
    - Enter in terminal: `0 12 * * * /path/to/python /path/to/ms_rewards.py --headless --mobile --pc --quiz`


## Troubleshooting

If the bot had worked before but stopped working all of a sudden, this may because I added new dependency. In this case, try this to see if the problem is solved:

- Enter into cmd/terminal/shell: `python -m pip install -r requirements.txt`

## To Do

- High priority:
  - Better logging
  - Simplify exception handling
- Low priority:
  - Support for other regions

## License

100% free to use and open source. :see_no_evil: :hear_no_evil: :speak_no_evil:

## Versions

For a summary of changes in each version of the bot, please see
**[CHANGELOG](READMEs/CHANGELOG.md).**

#### Credit

@LjMario007 - for previous developments<br />
@blackluv - for the original idea and developments<br />
@ShoGinn - for extraordinary assistance in making this project better!
