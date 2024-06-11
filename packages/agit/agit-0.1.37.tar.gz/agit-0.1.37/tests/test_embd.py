#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2024/04/11 11:38:48
@Author  :   ChenHao
@Description  :  测试embedding模型
@Contact :   jerrychen1990@gmail.com
'''


import os
from unittest import TestCase
from agit.embd import EMBD_TYPE, call_embedding
from loguru import logger
from agit.utils import cal_vec_similarity
from snippets import set_logger


# unit test
class TestEMBD(TestCase):

    @classmethod
    def setUpClass(cls):
        set_logger("dev", __name__)
        logger.info("start test embd")

    def test_zhipu_api(self):
        # set_logger("dev", "")
        texts = ["你好", "hello"]
        embds = call_embedding(text=texts, model_or_url="embedding-2", embd_type=EMBD_TYPE.ZHIPU_API,
                               norm=False, batch_size=4, api_key=os.environ["ZHIPU_API_KEY"])
        logger.info(len(embds))
        self.assertEqual(len(embds), 2)
        import numpy as np
        logger.info(np.linalg.norm(embds[0]))
        self.assertAlmostEqual(np.linalg.norm(embds[0]), 1.0)

        logger.info(embds[0][:4])
        embd = call_embedding(text=texts[0], model_or_url="embedding-2", embd_type=EMBD_TYPE.ZHIPU_API,
                              norm=True, batch_size=4, api_key=os.environ["ZHIPU_API_KEY"])
        logger.info(embd[:4])
        
        l2_distance = cal_vec_similarity(embds[0], embd, metric="l2_distance")

        logger.info(f"{l2_distance=}")
        self.assertAlmostEquals(l2_distance, 0.)


    def test_local_embd(self):
        url = "http://hz-model.bigmodel.cn/embedding-models/v2/embeddings"
        texts = ["你好", "hello"]
        embds = call_embedding(text=texts, model_or_url=url , embd_type=EMBD_TYPE.LOCAL,
                               norm=False, batch_size=4)
        logger.info(len(embds))
        self.assertEqual(len(embds), 2)
        import numpy as np
        logger.info(np.linalg.norm(embds[0]))
        self.assertNotAlmostEquals(np.linalg.norm(embds[0]), 1.0)

        logger.info(embds[0][:4])
        embd = call_embedding(text=texts[0], model_or_url=url, embd_type=EMBD_TYPE.LOCAL,
                              norm=True, batch_size=4)
        logger.info(embd[:4])
        cosine_simi = cal_vec_similarity(embds[0], embd)
        
        logger.info(f"cosine similarity: {cosine_simi}")
        self.assertAlmostEquals(cosine_simi, 1.)