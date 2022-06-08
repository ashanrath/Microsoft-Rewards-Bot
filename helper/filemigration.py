
import os
import shutil

def migrate_from_older_version():
    if not os.path.isdir('options'):
        os.mkdir('options')

    if os.path.isfile('ms_rewards_login_dict.json'):
        shutil.move('ms_rewards_login_dict.json', 'options/login_cred.json')

    if os.path.isfile('ms_rewards_redeem_options.json'):
        shutil.move('ms_rewards_redeem_options.json', 'options/redeem_options.json')

    if os.path.isfile('ms_rewards_telegram_bot.json'):
        shutil.move('ms_rewards_telegram_bot.json', 'options/telegram_bot.json')