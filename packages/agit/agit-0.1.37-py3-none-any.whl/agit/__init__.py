#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/08/15 11:11:03
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''
import os
from loguru import logger
from snippets import print_info, set_logger

AGIT_ENV = os.environ.get("AGIT_ENV", "dev")

AGIT_HOME = os.environ.get("AGIT_HOME")
if not AGIT_HOME:
    if "HOME" not in os.environ:
        raise RuntimeError("agit模块启动失败，请设置AGIT_HOME环境变量或者HOME环境变量")
    HOME = os.environ["HOME"]
    AGIT_HOME = os.path.join(HOME, ".agit")
    

AGIT_LOG_HOME = os.path.join(AGIT_HOME, "logs")
os.makedirs(AGIT_LOG_HOME, exist_ok=True)


set_logger(env=AGIT_ENV, module_name=__name__, log_dir=AGIT_LOG_HOME)


def show_env():
    print_info("current AGIT env", logger)
    logger.info(f"{AGIT_ENV=}")
    logger.info(f"{AGIT_HOME=}")
    logger.info(f"{AGIT_LOG_HOME=}")
    print_info("", logger)


show_env()
