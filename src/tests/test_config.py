#!/usr/bin/env python3

import os
from util.config import Config


def test_path():
    config = Config()
    assert os.path.exists(config.config_file)


def test_configuration_file():
    config = Config()
    config_obj = config.get_config()
    assert type(config_obj) is dict
    assert type(config_obj['bridge']['ip']) is str
    assert type(config_obj['bridge']['user']) is str
    assert type(config_obj['lights']) is list
