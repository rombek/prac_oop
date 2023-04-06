import datetime
from enum import Enum
import logging
import sys
from pathlib import Path

HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60
MINUTES_PER_DAY = HOURS_PER_DAY * MINUTES_PER_HOUR

TOTAL_MODELLING_MINUTES = 2 * 7 * MINUTES_PER_DAY


class Weekday(int, Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def get_logger():
    logs_path = Path('./logs')
    logs_path.mkdir(exist_ok=True)
    logging.basicConfig(
        filemode='w',
        format='[%(levelname)s] %(message)s',
        filename=logs_path / f'{datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.txt',
        level=logging.DEBUG,
        encoding='utf-8',
    )
    logger = logging.getLogger(__name__)
    # if not getattr(logger, 'handler_set', None):
    #     logger.setLevel(logging.DEBUG)
    #     handler.setFormatter(logging.Formatter(fmt='[%(levelname)s] %(message)s'))
    #     logger.addHandler(handler)

    return logger


logger = get_logger()
