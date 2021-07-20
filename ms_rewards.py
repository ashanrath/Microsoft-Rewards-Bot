import argparse
import json
import logging
from msreward.msr import MSR
import os
import platform

from selenium.common.exceptions import WebDriverException
from helper.logger import *
from helper.driver import update_driver


msr_version = 'v2.0a'

def check_python_version():
    """
    Ensure the correct version of Python is being used.
    """
    minimum_version = ('3', '9')
    if platform.python_version_tuple() < minimum_version:
        message = 'Only Python %s.%s and above is supported.' % minimum_version
        raise Exception(message)


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
    _parser = arg_parser.parse_args()
    if _parser.all_mode:
        _parser.mobile_mode = True
        _parser.pc_mode = True
        _parser.quiz_mode = True
    return _parser


def get_login_info():
    with open('ms_rewards_login_dict.json', 'r') as f:
        return json.load(f)


if __name__ == '__main__':
    check_python_version()
    if os.path.exists("drivers/chromedriver.exe"):
        update_driver()
    try:
        # argparse
        parser = parse_args()

        # start logging
        init_logging(log_level=parser.log_level)
        logging.info(msg='--------------------------------------------------')
        logging.info(msg='-----------------------New------------------------')
        logging.info(msg='--------------------------------------------------')
        logging.info(msg=f'Bot version: {msr_version}')

        login_cred = get_login_info()
        logging.info(msg=f'logins retrieved, {len(login_cred)} account(s):')
        for cred in login_cred:
            logging.info(msg=f'{cred["email"]}')

        msrs = [MSR(x['email'], x['password'], x['secret'] if 'secret' in x else None, parser.headless)
                for x in login_cred]

        for msr in msrs:
            logging.info(
                msg='--------------------------------------------------')
            logging.info(msg=f'Current account: {msr.email}')
            msr.work(flag_pc=parser.pc_mode, flag_mob=parser.mobile_mode,
                     flag_quiz=parser.quiz_mode)

    except WebDriverException:
        logging.exception(msg='Failure at main()')
