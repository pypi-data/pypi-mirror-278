#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/09/11 10:19:27
@Author  :   ChenHao
@Contact :   jerrychen1990@gmail.com
'''


import copy
import itertools
import os
from typing import Any, List, Union
from cachetools import LRUCache, cached
from loguru import logger

import numpy as np
import zhipuai
from agit import AGIT_LOG_HOME
from snippets import retry, jdumps
from zhipuai import ZhipuAI


from agit.utils import gen_req_id

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


def resp_generator(events, max_len=None, err_resp=None):
    token_left = max_len if max_len else None
    for event in events:
        if event.event == "add":
            if token_left:
                if len(event.data) > token_left:
                    data = event.data[:token_left]
                else:
                    data = event.data
                token_left -= len(data)
                yield data
                if token_left == 0:
                    break
            else:
                yield event.data
        elif event.event == "finish":
            pass
        else:
            default_logger.error(
                f"zhipu api resp failed with event:{event.event}, data:{event.data}")
            yield err_resp if err_resp else event.data


def support_system(model: str):
    return model.startswith("chatglm3") or model in ["glm-4", "glm-3-turbo", "glm-4v"]


def resp2generator_v4(resp, logger, request_id):
    tool_calls = None
    acc_chunks = []

    for chunk in resp:
        choices = chunk.choices
        if choices:
            choice = choices[0]
            tool_calls = choice.delta.tool_calls
            acc_chunks.append(chunk)
        break
    # print(acc_chunks)

    def gen():
        acc = []
        for chunk in itertools.chain(acc_chunks, resp):
            choices = chunk.choices
            if choices:
                choice = choices[0]
                if choice.delta.content:
                    delta_content = choice.delta.content
                    yield delta_content
                    acc.append(delta_content)
        resp_msg = "".join(acc).strip()
        with logger.contextualize(request_id=request_id):
            logger.debug(f"model generate answer:{resp_msg}")

    return tool_calls, gen()


@cached(LRUCache(maxsize=1000))
def get_client(api_key: str) -> ZhipuAI:
    logger.info(f"new zhipuai client with {api_key=}")
    client = ZhipuAI(api_key=api_key or os.environ.get("ZHIPU_API_KEY"))
    return client


def _is_multimodal(model:str):
    return model in ["glm-4v"]
    
    

def build_messages(prompt: Union[str, dict], model:str, system:str, history:List[dict], role:str, image_url:str, logger):
    if isinstance(prompt, dict):
        messages = history + [prompt]
    else:
        if image_url and _is_multimodal(model):
            message = dict(role=role, content=[dict(type="text", text=prompt), dict(type="image_url", image_url=dict(url=image_url))])
        else:
            message = dict(role=role, content=prompt)
        
        messages = history + [message]   
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
    


def call_llm_api(prompt: Union[str, dict], model: str, api_key=None, role="user", image_url:str=None,
                 system=None, history=[], tools=[], do_search=False, search_query=None,
                 logger=None, stream=True, return_origin=False, return_tool_call=False, **kwargs) -> Any:
    import inspect
    if "request_id" not in kwargs:
        request_id = gen_req_id(prompt=prompt, model=model)
        kwargs.update(request_id=request_id)
    request_id = kwargs["request_id"]
    the_logger = logger if logger else default_logger
    
    with the_logger.contextualize(request_id=request_id):
        client = get_client(api_key=api_key or os.environ.get("ZHIPU_API_KEY"))
        valid_keys = dict(inspect.signature(client.chat.completions.create).parameters).keys()
        messages = build_messages(prompt=prompt, model=model, system=system, image_url=image_url, history=history, role=role, logger=the_logger)

        tools = copy.copy(tools)

        if not do_search and model=="glm-4":
            close_search_tool = {'type': 'web_search', 'web_search': {'enable': False, 'search_query': search_query}}
            tools.append(close_search_tool)
            # the_logger.debug(f"adding close search tool")

        kwargs = {k: v for k, v in kwargs.items() if k in valid_keys}
        # 处理temperature=0的特殊情况
        if kwargs.get("temperature") == 0:
            kwargs.pop("temperature")
            kwargs["do_sample"] = False

        api_inputs = dict(model=model,
                          messages=messages,
                          tools=tools,
                          stream=stream,
                          **kwargs)
        the_logger.debug(f"api_inputs:\n{jdumps(api_inputs)}")

        if return_origin:
            resp = client.chat.completions.create(
                **api_inputs
            )
            the_logger.info(f"api origin resp:{resp}")
            return resp

        api_inputs.update(stream=True)
        response = client.chat.completions.create(
            **api_inputs
        )
        # usage = response.usage
        # the_logger.debug(f"token usage: {usage}")

        tool_call, resp_gen = resp2generator_v4(response, logger=the_logger, request_id=request_id)

        if not stream:
            resp_gen = "".join(resp_gen)
        if return_tool_call:
            return tool_call, resp_gen

        return resp_gen


def call_character_api(prompt: str, user_name, user_info, bot_name, bot_info,
                       history=[], model="characterglm", api_key=None, stream=True, max_len=None, **kwargs):
    check_api_key(api_key)
    zhipu_prompt = history + [dict(role="user", content=prompt)]
    total_words = sum([len(e['content']) for e in zhipu_prompt])
    default_logger.debug(f"zhipu prompt:")
    detail_msgs = []

    for idx, item in enumerate(zhipu_prompt):
        detail_msgs.append(f"[{idx+1}].{item['role']}:{item['content']}")
    default_logger.debug("\n"+"\n".join(detail_msgs))
    default_logger.debug(
        f"{model=},{kwargs=}, history_len={len(history)}, words_num={total_words}")
    meta = {
        "user_info": user_info,
        "bot_info": bot_info,
        "bot_name": bot_name,
        "user_name": user_name
    }
    response = zhipuai.model_api.sse_invoke(
        model=model,
        meta=meta,
        prompt=zhipu_prompt,
        incremental=True,
        ** kwargs
    )
    generator = resp_generator(response.events(), max_len=None)
    if stream:
        return generator
    else:
        resp = "".join(list(generator)).strip()
        if max_len:
            resp = resp[:max_len]
        return resp


def call_embedding_api(text: str, api_key=None, model="embedding-2",
                       norm=None, retry_num=2, wait_time=(1,2)):
    client = get_client(api_key=api_key or os.environ.get("ZHIPU_API_KEY"))

    def zhipu_embedding_attempt():
        resp = client.embeddings.create(
            model=model,  # 填写需要调用的模型名称
            input=text,
        )
        embedding = resp.data[0].embedding
        if norm is not None:
            _norm = 2 if norm == True else norm
            embedding = embedding / np.linalg.norm(embedding, _norm)
        return embedding

    if retry_num:
        attempt = retry(retry_num=retry_num, wait_time=wait_time)(zhipu_embedding_attempt)
    return attempt()


def call_image_gen(prompt: str, api_key: str = None) -> str:
    client = get_client(api_key=api_key or os.environ.get("ZHIPU_API_KEY"))

    response = client.images.generations(
        model="cogview-3",  # 填写需要调用的模型名称
        prompt=prompt,
    )
    return response.data[0].url


if __name__ == "__main__":
    text = "你好"
    system = "你是孔子，请以文言文回答我"
    resp = "".join(call_llm_api(model="chatglm3_130b_int8", prompt=text, system=system, stream=False))
    print(resp)
    emb = call_embedding_api(text)
    print(len(emb))
    print(emb[:4])
