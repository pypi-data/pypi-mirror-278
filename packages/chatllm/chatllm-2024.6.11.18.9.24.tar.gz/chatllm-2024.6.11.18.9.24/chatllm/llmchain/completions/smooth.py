#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : copilot
# @Time         : 2023/12/6 13:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


import openai

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.smooth_queue import SmoothQueue

from meutils.notice.feishu import send_message

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from chatllm.llmchain.completions import openai_completions
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.utils.openai_utils import to_openai_completion_params, openai_response2sse
from chatllm.schemas.openai_types import chat_completion_chunk

from openai import OpenAI, AsyncOpenAI


class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')

        self.client = AsyncOpenAI(api_key=self.api_key)

    async def acreate(self, request: ChatCompletionRequest, **kwargs):
        data = to_openai_completion_params(request)

        start_time = time.perf_counter()

        try:
            # _ = await self.client.chat.completions.create(**data)

            async def gen():
                async for chunks in await self.client.chat.completions.create(**data):
                    logger.debug(chunks)
                    if chunks.choices[0].finish_reason == 'stop':
                        yield chunks
                        return
                    for chunk in chunks:
                        chat_completion_chunk.choices[0].delta.content = chunk.choices[0].delta.content
                        yield chat_completion_chunk

            _ = gen()

        except Exception as e:
            logger.error(e)
            send_message(f"{self.api_key}\n{e}\n耗时：{time.perf_counter() - start_time} s", "Copilot Token 异常")

            data['model'] = 'backup-gpt'
            _ = await AsyncOpenAI().chat.completions.create(**data)

        if request.stream:
            return SmoothQueue().consumer(_, delay=0.05)

        return _


if __name__ == '__main__':
    Completions().acreate(ChatCompletionRequest(model='qwen-all'))
