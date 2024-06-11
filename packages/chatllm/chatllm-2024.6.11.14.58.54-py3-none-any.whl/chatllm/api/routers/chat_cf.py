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

from chatllm.completions.cf import Completions

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

    api_key = np.random.choice(api_key.strip().split(','))  # 轮询多个 api_key

    model_map = {
        "dreamshaper-8-lcm": "@cf/lykon/dreamshaper-8-lcm",
        "stable-diffusion-v1-5-img2img": "@cf/runwayml/stable-diffusion-v1-5-img2img",
        "stable-diffusion-v1-5-inpainting": "@cf/runwayml/stable-diffusion-v1-5-inpainting",
        "stable-diffusion-xl-base-1.0": "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        "stable-diffusion-xl-lightning": "@cf/bytedance/stable-diffusion-xl-lightning",
        "*": "@cf/bytedance/stable-diffusion-xl-lightning",
    }
    request.model = model_map.get(request.model, model_map["*"])  # 最快
    response = Completions(api_key).acreate(request)
    return openai_response2sse(response)


@router.post("/audio/transcriptions")
async def create_audio_transcriptions(
    file: Union[UploadFile] = File(...),  # 文件链接
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    # logger.debug(request)

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

    api_key = np.random.choice(api_key.strip().split(','))  # 轮询多个 api_key

    _ = await Completions(api_key).acreate_asr(file)

    return _


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
    # for i in range(10):
    #     send_message(f"兜底模型", title="github_copilot")
