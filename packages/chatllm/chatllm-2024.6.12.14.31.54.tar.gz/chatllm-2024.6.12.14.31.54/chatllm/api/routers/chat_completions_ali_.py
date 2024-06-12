#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : completions
# @Time         : 2023/12/19 16:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 逆向工程
import pandas as pd

from meutils.pipe import *
from meutils.notice.feishu import send_message
from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status
from starlette.background import BackgroundTask, BackgroundTasks

from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chatllm.completions.ali import Completions
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest

router = APIRouter()

ChatCompletionResponse = Union[ChatCompletion, List[ChatCompletionChunk]]

from meutils.llm.openai_utils import create_chat_completion_chunk
from sse_starlette import EventSourceResponse, ServerSentEvent


@router.post("/chat/completions")
async def create_chat_completions(
    request: ChatCompletionRequest,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
    # background_tasks: BackgroundTasks = ...
):
    # background_tasks.add_task(send_message, "response")
    logger.debug(request)

    api_key = auth and auth.credentials or None

    response = await Completions(api_key=api_key).acreate(request)

    async def agen():  # 不正常
        for i in response:
            yield i.model_dump_json()
            await asyncio.sleep(0)

    # sse_response
    return EventSourceResponse(
        create_chat_completion_chunk(response),
        # agen(),
        # background=BackgroundTask(send_message, "response"),
        ping=10000
    )


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
    # for i in range(10):
    #     send_message(f"兜底模型", title="github_copilot")
