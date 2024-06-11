#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/10 10:28:36
@Author  :   ChenHao
@Description  : 大模型接口
@Contact :   jerrychen1990@gmail.com
'''


from enum import Enum
import json
from typing import List


from agit.common import LLMResp, ToolDesc, LLMError
from agit.utils import gen_req_id
from loguru import logger
from snippets.logs import set_logger, ChangeLogLevelContext


class LLM_TYPE(str, Enum):
    ZHIPU_API = "ZHIPU_API"
    TGI = "TGI"


def call_llm(messages: List[dict], model: str = None, url=None, llm_type: LLM_TYPE = LLM_TYPE.ZHIPU_API,
             stream=True, system=None, temperature=0.7, top_p=0.95, max_tokens: int = 2048, do_sample=True,
             request_id: str = None, do_search=False, search_query=None, tools: List[ToolDesc] = [],
             log_level: str = None, details=False, **kwargs) -> LLMResp:
    if not request_id:
        request_id = gen_req_id(prompt=messages[-1]["content"], model=model)
    with ChangeLogLevelContext(module_name="agit", sink_type="stdout", level=log_level):
        try:
            if llm_type == LLM_TYPE.ZHIPU_API:
                from agit.backend.zhipu_api import call_llm as call_zhipu_api_llm
                resp: LLMResp = call_zhipu_api_llm(messages, model=model, system=system, stream=stream, temperature=temperature,
                                                   top_p=top_p, max_tokens=max_tokens, do_sample=do_sample, request_id=request_id,
                                                   do_search=do_search, search_query=search_query, tools=tools, **kwargs)
            if llm_type == LLM_TYPE.TGI:
                from agit.backend.local import call_tgi_llm
                resp: LLMResp = call_tgi_llm(messages, url=url, system=system, stream=stream, temperature=temperature,
                                             top_p=top_p, max_tokens=max_tokens, do_sample=do_sample, request_id=request_id, **kwargs)

            if not details:
                resp.details = None
            return resp
        except LLMError as error:
            raise error
        except Exception as e:
            logger.error(f"call llm failed, request_id: {request_id}, error: {e}, {type(e)=}, convert to LLMError")
            raise LLMError(status_code=500, message=str(e))


def call_text2image(prompt: str, model: str, log_level: str = None, llm_type: LLM_TYPE = LLM_TYPE.ZHIPU_API,
                    api_key: str = None, request_id=None, details=False, **kwargs) -> LLMResp:
    if not request_id:
        request_id = gen_req_id(prompt=prompt, model=model)
    with ChangeLogLevelContext(module_name="agit", sink_type="stdout", level=log_level):
        if llm_type == LLM_TYPE.ZHIPU_API:
            from agit.backend.zhipu_api import call_text2image as call_zhipu_api_text2image
            resp: LLMResp = call_zhipu_api_text2image(prompt=prompt, api_key=api_key)
        if not details:
            resp.details = None
        return resp


if __name__ == "__main__":
    set_logger("dev", "__main__")
    messages = [dict(role="user", content="你好呀，你是谁")]
    _system = "请用英语回答我的问题，你的名字叫XAgent"
    # 测试zhipu api
    resp = call_llm(messages, model="glm-3-turbo", system=_system, temperature=0.7, top_p=0.95, max_tokens=100, stream=False)
    logger.info(json.dumps(resp.model_dump(), ensure_ascii=False, indent=4))
    # 流式
    resp = call_llm(messages, model="glm-3-turbo", system=_system, temperature=0.7, top_p=0.95, max_tokens=100, log_level="INFO", stream=True)
    for chunk in resp.content:
        logger.info(chunk)
    logger.info(json.dumps(resp.model_dump(exclude={"content"}), ensure_ascii=False, indent=4))
