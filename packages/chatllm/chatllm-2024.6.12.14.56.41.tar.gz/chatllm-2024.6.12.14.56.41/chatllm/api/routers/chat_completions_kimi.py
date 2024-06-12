#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : completions
# @Time         : 2023/12/19 16:38
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 逆向工程
# todo: llm2gpt

from meutils.pipe import *
from meutils.notice.feishu import send_message
from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

from sse_starlette import EventSourceResponse
from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status

from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chatllm.llmchain.completions import kimi
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.utils.openai_utils import openai_response2sse

router = APIRouter()

ChatCompletionResponse = Union[ChatCompletion, List[ChatCompletionChunk]]


@router.post("/chat/completions")
async def create_chat_completions(
    request: ChatCompletionRequest,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    logger.debug(request)

    api_key = auth and auth.credentials or None
    if api_key is None:
        detail = {
            "error": {
                "message": "",
                "type": "invalid_request_error",
                "param": None,
                "code": "invalid_api_key",
            }
        }
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    # 轮询
    api_keys = api_key.strip().split('|')
    api_key = api_keys[0] if len(api_keys) == 1 else np.random.choice(api_keys)

    # kimi kimi-128k kimi-all rag-kimi
    # moonshot-v1-8k moonshot-v1-32k moonshot-v1-128k
    if request.model == "kimi-all" and request.messages[-1]["content"].strip().startswith(("画",)):
        # 增加画图功能
        response = await AsyncOpenAI().chat.completions.create(
            model="gpt-4-mobile",
            messages=request.messages[-1:],
            stream=True
        )
        return openai_response2sse(response, redirect_model=request.model)

    if request.file_ids or request.model == 'kimi-me':  # todo: 根据fileid映射对应的refresh_token
        # 增加计费
        request.use_search = False
        completions = kimi.Completions()

    elif request.model.startswith(("moonshot",)):
        request.use_search = False
        completions = kimi.Completions(api_key=api_key)
    else:
        completions = kimi.Completions(api_key=api_key)

    response = completions.create_sse(request)
    return response


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
    # for i in range(10):
    #     send_message(f"兜底模型", title="github_copilot")
