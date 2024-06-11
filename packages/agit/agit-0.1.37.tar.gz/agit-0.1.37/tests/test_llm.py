#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/11 10:52:54
@Author  :   ChenHao
@Description  : 测试llm接口
@Contact :   jerrychen1990@gmail.com
'''

import json
from unittest import TestCase
from agit.common import LLMError, LLMResp, Parameter, ToolDesc
from agit.llm import LLM_TYPE, call_llm, call_text2image
from loguru import logger
from snippets import set_logger


# unit test
class TestLLM(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start llm")
        cls.tgi_12b_url = "http://hz-model.bigmodel.cn/tgi-12b"

    def test_zhipu_api(self):
        # set_logger("dev", "")
        messages = [dict(role="user", content="你好呀，你是谁")]
        _system = "请用英语回答我的问题，你的名字叫XAgent"
        # 测试zhipu api
        resp = call_llm(messages, model="glm-3-turbo", system=_system, temperature=0.7, top_p=0.95, max_tokens=100, stream=False)
        logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.content)
        self.assertIsNotNone(resp.usage)

        # 流式
        resp = call_llm(messages, model="glm-3-turbo", system=_system, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=True)
        for chunk in resp.content:
            logger.info(chunk)
        logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.usage)

    def test_zhipu_api_sensitive(self):
        # set_logger("dev", "")
        logger.info("test sensitive call")
        with self.assertRaises(LLMError) as context:
            _system = None
            messages = [dict(role="user", content="评价一下习近平")]
            # 测试zhipu api
            resp = call_llm(messages, model="glm-3-turbo", system=_system, temperature=0.7, top_p=0.95, max_tokens=100, stream=False)
            # logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
            self.assertIn("敏感内容", context.exception.message)
            # self.assertIsNotNone(resp.usage)

        # # 流式
        logger.info("test sensitive call stream")
        resp = call_llm(messages, model="glm-3-turbo", system=_system, temperature=0.7, top_p=0.95, max_tokens=100, stream=True)
        acc_content = ""
        for chunk in resp.content:
            logger.info(chunk)
            acc_content += chunk
        logger.info(acc_content)
        self.assertIn("敏感内容", acc_content)

    def test_zhipu_api_tool_call(self):
        travel_tool = ToolDesc(name="query_train_info", description="根据用户提供的信息，查询对应的车次",
                               parameters=[Parameter(name="departure", description="出发城市或车站", type="string", required=True),
                                           Parameter(name="destination", description="目的地城市或车站", type="string", required=True),
                                           Parameter(name="date", description="要查询的车次日期", type="string", required=True)])

        messages = [dict(role="user", content="你能帮我查询2024年1月1日从北京南站到上海的火车票吗？")]
        _system = None
        # 测试zhipu api
        resp = call_llm(messages, model="glm-3-turbo", system=_system, tools=[travel_tool], temperature=0.7, top_p=0.95, max_tokens=100, stream=False)
        logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.tool_calls)
        self.assertIsNotNone(resp.usage)

        # 流式
        resp = call_llm(messages, model="glm-3-turbo", system=_system,
                        tools=[travel_tool], temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=True)
        for chunk in resp.content:
            logger.info(chunk)
        logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))

        self.assertIsNotNone(resp.tool_calls)
        self.assertIsNotNone(resp.usage)

    def test_local_tgi_v2(self):
        logger.info("test_local_tgi_api")
        # set_logger("dev", "")
        messages = [dict(role="user", content="你好呀，你是谁")]
        # 测试tgi api
        logger.info("test sync chat")
        resp = call_llm(messages, url=self.tgi_12b_url, llm_type=LLM_TYPE.TGI, version="v2",
                        temperature=0.7, top_p=0.95, max_tokens=100, stream=False, do_sample=False)
        logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.content)
        # self.assertTrue("GLM" in resp.content)

    def test_local_tgi_v2_stream(self):
        messages = [dict(role="user", content="你好呀，你是谁")]

        # 测试流式
        # 流式
        logger.info("test stream chat")
        resp = call_llm(messages, url=self.tgi_12b_url, llm_type=LLM_TYPE.TGI, temperature=0.7, version="v2",
                        top_p=0.95, max_tokens=100, stream=True, do_sample=False)

        acc = []
        for chunk in resp.content:
            logger.info(chunk)
            acc.append(chunk)

        full_response = "".join(acc)
        logger.info(f"full response:{full_response}")
        logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))
        self.assertIsNotNone(resp.usage.completion_tokens)
        self.assertIsNotNone(full_response)

    def test_local_tgi_v2_multiturn(self):

        logger.info("test multi turn chat")
        questions = ["推荐三首歌", "介绍一下第三首"]
        messages = []
        for question in questions:
            messages.append(dict(role="user", content=question))
            resp = call_llm(messages, url=self.tgi_12b_url, llm_type=LLM_TYPE.TGI, version="v2",
                            temperature=0.7, top_p=0.95, max_tokens=100, stream=True, do_sample=False)

            acc = []
            for chunk in resp.content:
                logger.info(chunk)
                acc.append(chunk)

            full_response = "".join(acc)
            logger.info(f"full response:{full_response}")
            messages.append(dict(role="assistant", content=full_response))
            logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))
            self.assertIsNotNone(resp.usage.completion_tokens)
            self.assertIsNotNone(full_response)

    def test_zhipu_api_text2image(self):
        prompt = "画一只皮卡丘和一只可达鸭，扁平风格"
        resp: LLMResp = call_text2image(prompt, model="cogview-3", log_level="INFO")
        logger.info(resp.image)
