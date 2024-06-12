# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

import os
from loguru import logger
from aac_init.conf import settings


def setup_logging():
    logger.add(
        sink=os.path.join(
            settings.OUTPUT_BASE_DIR,
            'aac_init_log',
            'aac_init_main.log'
        ),
        format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
        encoding='utf-8'
    )

    return logger
