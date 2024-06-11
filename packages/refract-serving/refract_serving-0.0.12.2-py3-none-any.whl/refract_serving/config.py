# -*- coding: utf-8 -*-
import configparser
import os


# config file
config_file = os.getenv(
    "MOSAIC_AI_SETTINGS",
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "configs",
        "local.ini",
    ),
)


# define config parser
config = configparser.ConfigParser(allow_no_value=True)
config.read(config_file)
