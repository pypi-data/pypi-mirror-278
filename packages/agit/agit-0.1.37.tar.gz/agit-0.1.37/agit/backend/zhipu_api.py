#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/10 11:07:17
@Author  :   ChenHao
@Description  :   智谱api
@Contact :   jerrychen1990@gmail.com
'''

import inspect
import itertools
import json
import time
from typing import Any, Iterable, List, Tuple

import numpy as np
import zhipuai.core
import zhipuai.core._errors

from agit.common import LLMResp, Perf, ToolCall, ToolDesc, Usage, LLMError

from loguru import logger
import os
from typing import List
from cachetools import LRUCache, cached
from loguru import logger

import zhipuai
from agit import AGIT_LOG_HOME
from snippets import jdumps, retry, batch_process
from zhipuai import ZhipuAI


fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level: <8}</level>|  - <level>[{extra[request_id]}]{message}</level>"

logger.add(os.path.join(AGIT_LOG_HOME, "zhipuai_bk.log"), retention="365 days", rotation=" 00:00", level="DEBUG", format=fmt,
           filter=lambda r: r["function"] == "call_llm_api_v4")

default_logger = logger


def check_api_key(api_key):
    if api_key is None:
        api_key = os.environ.get("ZHIPUAI_API_KEY", None)
    if not api_key:
        raise ValueError("未设置api_key且未设置ZHIPUAI_API_KEY环境变量")
    zhipuai.api_key = api_key


@cached(LRUCache(maxsize=1000))
def get_client(api_key: str, timeout=120) -> ZhipuAI:
    # logger.debug(f"new zhipuai client with {api_key=}")
    client = ZhipuAI(api_key=api_key or os.environ.get("ZHIPU_API_KEY"), timeout=timeout)
    return client


def support_system(model: str):
    return model.startswith("chatglm3") or model in ["glm-4", "glm-3-turbo", "glm-4v"]


def _is_multimodal(model: str):
    return model in ["glm-4v"]


def build_messages(messages: List[dict], model: str, system: str):
    if system:
        if support_system(model):
            messages = [dict(role="system", content=system)] + messages
        else:
            logger.warning(f"{model} not support system message, system argument will not work")

    detail_msgs = []
    for idx, item in enumerate(messages):
        detail_msgs.append(f"[{idx+1}].{item['role']}:{item['content']}")
    logger.debug("\n"+"\n".join(detail_msgs))

    return messages


def resp2generator(api_resp: Iterable, first_chunk, request_id: str, usage: Usage):
    def gen():
        acc = []
        for chunk in itertools.chain([first_chunk], api_resp):
            choices = chunk.choices
            if choices:
                choice = choices[0]
                if choice.delta.content:
                    delta_content = choice.delta.content
                    # logger.info(f"{delta_content}")
                    yield delta_content
                    acc.append(delta_content)
            _usage = chunk.usage
            if _usage:
                usage.__dict__.update(_usage.model_dump())
            _finish_reason = choice.finish_reason
            if _finish_reason:
                if _finish_reason == "sensitive":
                    logger.warning(f"zhipu api finish with reason {_finish_reason}")
                    msg = "系统检测到输入或生成内容可能包含不安全或敏感内容，请您避免输入易产生敏感内容的提示语，感谢您的配合。"
                    acc.append(msg)
                    yield msg

        resp_msg = "".join(acc).strip()
        with logger.contextualize(request_id=request_id):
            logger.debug(f"model generate answer:{resp_msg}")

    return gen()


def build_tool_calls(tool_calls) -> List[ToolCall]:
    # logger.debug(f"tool_calls: {tool_calls}")
    if tool_calls is None:
        return []
    rs = []
    for tool_call in tool_calls:
        parameters = json.loads(tool_call.function.arguments)

        tmp = ToolCall(tool_call_id=tool_call.id, name=tool_call.function.name, parameters=parameters)
        rs.append(tmp)
    # logger.debug(f"tool_calls: {rs}")
    return rs


def _convert_tool_desc(tools: List[ToolDesc]) -> List[dict]:
    resp = []
    for tool in tools:

        properties = {p.name: dict(type=p.type, description=p.description) for p in tool.parameters}
        required = [p.name for p in tool.parameters if p.required]
        parameters = dict(type="object", properties=properties, required=required)
        tool_desc = dict(type="function", function=dict(name=tool.name, description=tool.description, parameters=parameters))
        resp.append(tool_desc)

    return resp


def _extract_tool_calls(api_resp, st: int) -> Tuple[List[ToolCall], Any]:
    tool_calls = []
    for chunk in api_resp:
        choices = chunk.choices
        first_token_latency = time.time() - st
        if choices:
            choice = choices[0]
            tool_calls = choice.delta.tool_calls
            tool_calls = build_tool_calls(tool_calls)
        break
    return tool_calls, chunk, first_token_latency


def _default_search(model: str):
    return model in ["glm-4", "chatglm3-6b-high"]


def call_llm(messages: List[str], model: str, request_id: str,
             system=None, stream=True, api_key=None,
             do_search=False, search_query=None, tools: List[ToolDesc] = [],
             temperature=0.7, top_p=0.95, max_tokens: int = None, do_sample=True, timeout=120,
             do_perf=False, **kwargs) -> LLMResp:

    st = time.time()
    try:
        with logger.contextualize(request_id=request_id):
            client = get_client(api_key=api_key or os.environ.get("ZHIPU_API_KEY"), timeout=timeout)
            messages = build_messages(messages=messages, model=model, system=system)

            tools = _convert_tool_desc(tools=tools)

            if not do_search and _default_search(model):
                close_search_tool = {'type': 'web_search', 'web_search': {'enable': False, 'search_query': search_query}}
                tools.append(close_search_tool)

            params = dict(temperature=temperature, top_p=top_p, max_tokens=max_tokens, do_sample=do_sample, **kwargs)
            # 处理temperature=0的特殊情况
            if params.get("temperature") == 0:
                params.pop("temperature")
                params["do_sample"] = False

            # 过滤无效的参数
            valid_keys = dict(inspect.signature(client.chat.completions.create).parameters).keys()
            params = {k: v for k, v in params.items() if k in valid_keys}

            api_inputs = dict(model=model,
                              messages=messages,
                              tools=tools,
                              stream=stream,
                              **params)
            logger.debug(f"api_inputs:\n{jdumps(api_inputs)}")
            details = dict(api_inputs=api_inputs, st=st)
            api_resp = client.chat.completions.create(
                **api_inputs
            )
            if stream:
                usage = Usage(total_tokens=None, completion_tokens=None, prompt_tokens=None)

                tool_calls, first_chunk, first_token_latency = _extract_tool_calls(api_resp=api_resp, st=st)

                content = resp2generator(api_resp, first_chunk, request_id, usage)
            else:
                logger.debug(f"api_outputs:\n{jdumps(api_resp)}")
                first_token_latency = None

                content = api_resp.choices[0].message.content
                tool_calls = build_tool_calls(api_resp.choices[0].message.tool_calls)
                usage = Usage.model_validate(api_resp.usage.model_dump())
                details.update(api_resp=api_resp)

            # logger.info(f"{usage=}, {type(usage)}")
            perf = None

            if do_perf:
                if stream:
                    content = (e for e in "".join(content))
                if usage.total_tokens is None:
                    logger.warning("usage.total_tokens is None, can't calculate perf!")
                else:
                    total_cost = time.time()-st
                    overall_speed = usage.total_tokens / total_cost
                    perf_dict = dict(total_cost=total_cost, overall_speed=overall_speed)
                    if first_token_latency:
                        encode_speed = usage.prompt_tokens / first_token_latency
                        decode_speed = usage.completion_tokens / (total_cost - first_token_latency)
                        perf_dict.update(encode_speed=encode_speed, decode_speed=decode_speed, first_token_latency=first_token_latency)
                    perf = Perf(**perf_dict)

            resp = LLMResp(content=content, details=details, usage=usage, tool_calls=tool_calls, perf=perf)
            return resp
    except zhipuai.core._errors.APIRequestFailedError as e:
        json_data = e.response.json()

        # json_data = e.json_data()
        # logger.error(f"{json_data=}")
        message = json_data["error"]["message"]
        error = LLMError(status_code=e.status_code, message=message)
        # logger.info(f"raise error :{error}")
        raise error
    except Exception as e:
        logger.error(f"zhipu pi get exception {type(e)=}, {e=}, convert it to llm_error")
        error = LLMError(status_code=500, msg=str(e))
        raise error


def _call_embedding_single(text: str, api_key: str = None, model: str = "embedding-2",
                           norm=True, retry_num=2, wait_time=(1, 2), **kwargs) -> List[float]:
    client = get_client(api_key=api_key or os.environ.get("ZHIPU_API_KEY"))

    def zhipu_embedding_attempt():
        try:
            resp = client.embeddings.create(
                model=model,  # 填写需要调用的模型名称
                input=text
            )
            embedding = resp.data[0].embedding
            if norm:
                embedding = embedding / np.linalg.norm(embedding, 2)
                embedding = embedding.tolist()
            return embedding
        except Exception as e:
            text_sample = text[:20]
            msg = f"calling zhipu api embedding with get error: {e}, with {text_sample=}, {len(text)=}, {model=}"

            # logger.error(msg)
            raise Exception(msg)

    if retry_num:
        attempt = retry(retry_num=retry_num, wait_time=wait_time)(zhipu_embedding_attempt)
    return attempt()


def call_embedding(text: str | List[str], api_key: str = None, model: str = "embedding-2",  norm=True,
                   batch_size=8, retry_num=2, wait_time=(1, 2)) -> List[float] | List[List[float]]:
    if isinstance(text, str):
        return _call_embedding_single(text=text, model=model, api_key=api_key, norm=norm, retry_num=retry_num, wait_time=wait_time)
    else:
        batch_embd_func = batch_process(work_num=batch_size, return_list=True)(_call_embedding_single)
        return batch_embd_func(data=text, model=model, api_key=api_key, norm=norm, retry_num=retry_num, wait_time=wait_time)


def call_text2image(prompt: str, model: str = "cogview-3", api_key: str = None) -> LLMResp:
    client = get_client(api_key=api_key or os.environ.get("ZHIPU_API_KEY"))

    response = client.images.generations(
        model=model,  # 填写需要调用的模型名称
        prompt=prompt,
    )
    logger.info(f"{response=}")
    url = response.data[0].url
    return LLMResp(content="", image=url)
