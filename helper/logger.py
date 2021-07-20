import argparse
import logging
import os
import pathlib

LOG_LEVEL_STRINGS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']


def log_level_string_to_int(log_level_string):
    log_level_string = log_level_string.upper()

    if log_level_string not in LOG_LEVEL_STRINGS:
        message = f'invalid choice: {log_level_string} (choose from {LOG_LEVEL_STRINGS})'
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)
    # check the logging log_level_choices have not changed from our expected values
    assert isinstance(log_level_int, int)
    return log_level_int


def init_logging(log_level):
    # gets dir path of python script, not cwd, for execution on cron
    os.chdir(pathlib.Path(__file__).resolve().parents[1])
    os.makedirs('logs', exist_ok=True)
    log_path = os.path.join('logs', 'ms_rewards.log')
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s :: %(levelname)-6s :: %(name)s :: %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ])
