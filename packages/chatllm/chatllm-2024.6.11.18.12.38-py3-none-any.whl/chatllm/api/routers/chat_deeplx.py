#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chat_deeplx
# @Time         : 2024/4/23 18:16
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.notice.feishu import send_message
from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status

from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chatllm.completions.deeplx import Completions

from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.utils.openai_utils import to_openai_completion_params, openai_response2sse

router = APIRouter()

ChatCompletionResponse = Union[ChatCompletion, List[ChatCompletionChunk]]

send_message = lru_cache(send_message)


@router.post("/chat/completions")
async def create_chat_completions(
    request: ChatCompletionRequest,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    logger.debug(request)
    raw_model = request.model

    response = Completions().create(request)
    if not request.stream:
        response = list(response)[0]
        if request.return_raw_response:  # 返回原生响应
            _ = response.choices[0].message.content
            return json.loads(_)

    return openai_response2sse(response, redirect_model=raw_model)


@router.post("/")  # https://api.deeplx.org/translate
async def create_chat_completions(
    request: ChatCompletionRequest,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    logger.debug(request)
    raw_model = request.model

    response = Completions().create(request)
    if not request.stream:
        response = list(response)[0]
        if request.return_raw_response:  # 返回原生响应
            _ = response.choices[0].message.content
            return json.loads(_)

    return openai_response2sse(response, redirect_model=raw_model)


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
    # for i in range(10):
    #     send_message(f"兜底模型", title="github_copilot")
