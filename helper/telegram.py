import json
import telegram
from telegram.utils.helpers import escape_markdown
from helper.logger import *
import math


def get_telegram_info():
    try:
        with open('ms_rewards_telegram_bot.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        logging.exception(msg='Telegram updates are enabled, but ms_rewards_telegram_bot.json not found.', exc_info=False)

    except Exception as e:
        logging.exception(msg=f'Telegram updates are enabled, but failed: {e}.')


def get_redeem_options():
    with open('ms_rewards_redeem_options.json', 'r') as f:
        return json.load(f)


def markdown_escape(message_text):
    # Remove special characters when passing exceptions to telegram.
    return escape_markdown(message_text, version=2)


def telegram_update(message_text):
    try:
        telegram_chats = get_telegram_info()
        for chat in telegram_chats:
            telegram_apikey = chat["telegram_apikey"]
            telegram_chatid = chat["telegram_chatid"]
            bot = telegram.Bot(token=telegram_apikey)
            bot.send_message(chat_id=telegram_chatid, text=(message_text), parse_mode="MarkdownV2")
    except TypeError:
        logging.exception(msg='Telegram updates are enabled, but failed to process ms_rewards_telegram_bot.json.', exc_info=False)
    except FileNotFoundError:
        logging.exception(msg='Telegram updates are enabled, but ms_rewards_telegram_bot.json not found.', exc_info=False)
    except Exception as e:
        logging.exception(msg='Telegram updates are enabled but failed to send.', exc_info=True)


def flag_checkbox(done_flag):
    return '☒' if done_flag else '☐'


def points_credit_value(points):
    try:
        redeem_options = get_redeem_options()
        message_list = []
        for option in redeem_options:
            available_value = str(math.floor(int(points)/int(option["price"]))*int(option["value"]))
            message_list.append(f'{option["currency"]}{available_value} {option["short_desc"]}')

        return '('+', '.join(message_list)+')'
    except FileNotFoundError as e:
        logging.info(msg='Skipped redemption value check, ms_rewards_redeem_options.json not found.', exc_info=False)
        return ''
    except Exception as e:
        logging.info(msg='Skipped redemption value check, failed to process file.', exc_info=False)
        return ''


def telegram_update_post_search(email, summary):
    email = markdown_escape(email)
    pc_flag = flag_checkbox(summary.pc_search_done)
    pc_c = summary.pc_search_progress
    pc_m = summary.pc_search_max
    mo_flag = flag_checkbox(summary.mob_search_done)
    mo_c = summary.mobile_search_progress
    mo_m = summary.mobile_search_max
    pu_flag = flag_checkbox(summary.punch_card_done)
    pu_c = summary.punch_card_progress
    pu_m = summary.punch_card_max
    qz_flag = flag_checkbox(summary.quiz_done)
    qz_c = summary.quiz_progress
    qz_m = summary.quiz_max
    points_credit_value_list = markdown_escape(points_credit_value(summary.available_points))

    telegram_message = (
        f'Update for {email}\n'
        f'```\n'
        f'    {pc_flag} PC  {pc_c}/{pc_m}  {pu_flag} Punch Card {pu_c}/{pu_m}\n'
        f'    {mo_flag} Mob {mo_c}/{mo_m}  {qz_flag} Quiz       {qz_c}/{qz_m}\n'
        f'```'
        f'Total Points:  {summary.available_points:,} {points_credit_value_list}'
    )
    telegram_update(telegram_message)
