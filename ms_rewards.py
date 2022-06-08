import argparse
import json
import logging
from helper.utils import hide_email
from msreward.msr import MSR
import os
import sys
import platform

from helper.filemigration import migrate_from_older_version
from helper.logger import *
from helper.driver import update_driver
from helper.telegram import *
import env


def check_python_version():
    """
    Ensure the correct version of Python is being used.
    """
    minimum_version = (3, 9)
    if sys.version_info < minimum_version:
        message = 'Only Python %s.%s and above is supported.' % minimum_version
        raise Exception
  
def parse_args():
    """
    Parses command line arguments for headless mode, mobile search, pc search, quiz completion
    :return: argparse object
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--headless',
        action='store_true',
        dest='headless',
        default=False,
        help='Activates headless mode, default is off.')
    arg_parser.add_argument(
        '--mobile',
        action='store_true',
        dest='mobile_mode',
        default=False,
        help='Activates mobile search, default is off.')
    arg_parser.add_argument(
        '--pc',
        action='store_true',
        dest='pc_mode',
        default=False,
        help='Activates pc search, default is off.')
    arg_parser.add_argument(
        '--quiz',
        action='store_true',
        dest='quiz_mode',
        default=False,
        help='Activates pc quiz search, default is off.')
    arg_parser.add_argument(
        '-a', '--all',
        action='store_true',
        dest='all_mode',
        default=False,
        help='Activates all automated modes (equivalent to --mobile --pc --quiz).')
    arg_parser.add_argument(
        '--log-level',
        default='INFO',
        dest='log_level',
        type=log_level_string_to_int,
        help=f'Set the logging output level. {LOG_LEVEL_STRINGS}')
    arg_parser.add_argument(
        '--exit-on-finish',
        action='store_true',
        dest='exit_on_finish',
        default=False,
        help='Script will exit when finishes, otherwise will remain open and wait for user to press enter to end.')
    arg_parser.add_argument(
        '--telegram',
        action='store_true',
        dest='telegram_message',
        default=False,
        help='Sends an update to telegram upon completion.')
    _parser = arg_parser.parse_args()
    if _parser.all_mode:
        _parser.mobile_mode = True
        _parser.pc_mode = True
        _parser.quiz_mode = True
    return _parser


def get_login_info():
    with open('options/login_cred.json', 'r') as f:
        return json.load(f)

def run_bot():
    migrate_from_older_version()
    parser = parse_args()

    check_python_version()
    if os.path.exists("drivers/chromedriver.exe"):
        update_driver()
    try:

        init_logging(log_level=parser.log_level)
        logging.info(msg='--------------------------------------------------')
        logging.info(msg='-----------------------New------------------------')
        logging.info(msg='--------------------------------------------------')
        logging.info(msg=f'Bot version: {env.BOT_VERSION}')

        login_cred = get_login_info()

        logging.info(msg=f'logins retrieved, {len(login_cred)} account(s):')
        for cred in login_cred:
            logging.info(msg=f'{hide_email(cred["email"])}')

        msrs = [MSR(x['email'], x['password'], x['secret'] if 'secret' in x else None, parser.headless)
                for x in login_cred]

        for msr in msrs:
            logging.info(
                msg='--------------------------------------------------')
            logging.info(msg=f'Current account: {hide_email(msr.email)}')
            msr.work(flag_pc=parser.pc_mode, flag_mob=parser.mobile_mode,
                     flag_quiz=parser.quiz_mode, flag_telegram=parser.telegram_message)


    except Exception:
        logging.exception('An error has occurred.', exc_info=True)
    finally:
        logging.info(msg='--------------------------------------------------')
        logging.info(msg='-----------------------End------------------------')
        logging.info(msg='--------------------------------------------------')
        if not parser.exit_on_finish:
            input('Press any key to exit...')


if __name__ == '__main__':
    run_bot()
