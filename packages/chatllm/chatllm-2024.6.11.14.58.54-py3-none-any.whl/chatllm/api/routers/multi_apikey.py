#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : multi_apikey
# @Time         : 2024/5/22 14:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.notice.feishu import send_message
from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

from sse_starlette import EventSourceResponse
from fastapi import APIRouter, File, UploadFile, Query, Form, Depends, Request, HTTPException, status, \
    BackgroundTasks as BT

from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chatllm.completions.multi_apikey import Completions
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

    # 轮询：先手动更新api keys
    logger.debug(api_key)

    base_url, feishu_url = api_key.split('|')  # {base_url}|{feishu_url}
    # https://api.deepseek.com/v1|https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=lVghgx

    client = Completions(base_url=base_url)
    background_tasks.add_task(client.get_and_update_api_keys, feishu_url)  # 5分钟更新一次 # 为啥会失效? #TODO
    # background_tasks.add_task(Completions().get_and_update_api_keys, feishu_url)  # 为啥会失效?
    # background_tasks.add_task(print, "############")  # 5分钟更新一次

    response = await client.acreate(request)  # todo: 缓存

    return openai_response2sse(response)
    # if request.stream:
    #     return openai_response2sse(response)

    # return response


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
    # for i in range(10):
    #     send_message(f"兜底模型", title="github_copilot")
