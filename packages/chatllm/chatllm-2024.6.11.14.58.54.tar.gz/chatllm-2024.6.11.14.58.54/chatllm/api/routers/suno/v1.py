#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : suno_api
# @Time         : 2024/5/29 15:43
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.llm.openai_utils import appu
from meutils.db.redis_db import redis_client
from meutils.notice.feishu import send_message
from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

from chatllm.schemas.suno_types import SunoRequest

from fastapi import APIRouter, File, UploadFile, Query, Form, Header, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter()


# @router.post("/music")
# async def e2e(
#     request: Request,
# ):
#     _ = await request.body()
#     send_message(_.decode())
#     return _
#     # return {"code": 200, "message": "success"}


@router.post("/music")
async def create_music(
    request: Request,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
    # x_api_key: Annotated[Union[List[str], None], Header()] = None,
):
    import json_repair

    request_data = json_repair.loads((await request.body()).decode())

    send_message(bjson(request_data), title="create_music")

    request = SunoRequest(**request_data)

    # logger.debug(request)
    logger.debug(request.input)

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

    async with httpx.AsyncClient(base_url="http://154.3.0.117:39955", follow_redirects=True) as client:
        if request.custom_mode:
            response = await client.post("/generate", json=request.input)

        else:
            response = await client.post("/generate/description-mode", json=request.input)

    data = response.json()
    # logger.debug(data)

    task_id = data.get("id")
    song_ids = ",".join([_.get('id') for _ in data.get("clips", [])])
    redis_client.set(f"task:{task_id}", song_ids, ex=3600 * 24 * 100)

    content = {
        "code": 200,
        "data": {
            "task_id": task_id,
        },
        "message": "success"
    }

    send_message(bjson(content), title="create_music")

    if response.is_success: await appu(api_key=api_key)
    return JSONResponse(content=content)


@router.get("/music/{task_id}")
async def get_music(
    task_id: str,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
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

    ids = redis_client.get(f"task:{task_id}").decode().split(',')
    clips = {}
    status_set = set()
    async with httpx.AsyncClient(base_url="http://154.3.0.117:39955", follow_redirects=True) as client:
        for song_id in ids:
            response = await client.get(f"/feed/{song_id}")
            clip = response.json()[0]
            clips[song_id] = clip
            status_set.add(clip.get("status"))

    content = {
        "code": 200,
        "data": {
            "task_id": task_id,
            "status": ",".join(status_set) + "d",
            "input": str(clip.get("metadata")),
            "clips": clips,
        },
        "message": "success"
    }
    if response.is_success and "complete" in status_set: await appu('ppu-0001', api_key=api_key)
    return JSONResponse(content=content)


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1/suno/v1')

    app.run()
