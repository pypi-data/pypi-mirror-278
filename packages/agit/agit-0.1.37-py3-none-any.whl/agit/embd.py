#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/11 10:36:39
@Author  :   ChenHao
@Description  :   请求embedding/rerank模型的入口
@Contact :   jerrychen1990@gmail.com
'''

from enum import Enum
import os
from typing import List

class EMBD_TYPE(str, Enum):
    ZHIPU_API = "ZHIPU_API"
    LOCAL = "LOCAL"
    


def call_embedding(text:str|List[str], model_or_url:str, embd_type: EMBD_TYPE = EMBD_TYPE.ZHIPU_API,
                   norm=True, batch_size=8, **kwargs)->List[float]|List[List[float]]:
    if embd_type == EMBD_TYPE.ZHIPU_API:
        from agit.backend.zhipu_api import call_embedding as call_zhipu_api_embedding    
        return call_zhipu_api_embedding(text=text, model=model_or_url, norm=norm, batch_size=batch_size, **kwargs)
    if embd_type == EMBD_TYPE.LOCAL:
        from agit.backend.local import call_embedding as call_local_embedding
        return call_local_embedding(text=text, url=model_or_url, norm=norm, batch_size=batch_size, **kwargs)
    raise ValueError(f"embd_type {embd_type} not supported")





if __name__ == "__main__":
    texts = ["你好", "hello"]
    embds = call_embedding(text=texts, model = "embedding-2", embd_type=EMBD_TYPE.ZHIPU_API,
                           norm=True, batch_size=4, api_key=os.environ["ZHIPU_API_KEY"])    
    print(len(embds))
    import numpy as np
    print(np.linalg.norm(embds[0]))
    print(embds[0][:4])

    embd = call_embedding(text=texts[0], model = "embedding-2", embd_type=EMBD_TYPE.ZHIPU_API,
                           norm=True, batch_size=4, api_key=os.environ["ZHIPU_API_KEY"])   
    print(embd[:4])




    



