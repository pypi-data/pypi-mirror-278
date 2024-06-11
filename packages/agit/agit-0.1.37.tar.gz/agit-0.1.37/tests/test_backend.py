#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/11/13 10:35:18
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''

import os
import sys
from unittest import TestCase

from agit.backend.zhipuai_bk import call_embedding_api, call_llm_api
from snippets import LoguruFormat
from loguru import logger

logger.add(sys.stdout, format=LoguruFormat.DETAIL, level="DEBUG", filter=__name__)
# unit test
class TestBackend(TestCase):
    def test_zhipu_backend(self):
        logger.info("test llm api")
        prompt = "你好"
        api_key = os.environ.get("ZHIHUPAI_API_KEY", "")
        resp = call_llm_api(prompt=prompt, model="glm-3-turbo", api_key=api_key, stream=False)
        logger.info(resp)
        logger.info("test embedding api")
        embd = call_embedding_api(text=prompt, api_key=api_key)
        logger.info(embd[:2])
        self.assertEqual(1024, len(embd))
        
