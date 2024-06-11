#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : files
# @Time         : 2023/12/29 14:21
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 返回链接，参考kimi，接入文档解析，16c32g机器部署，不能通服务调用, minio_client通用化 id 映射

from meutils.pipe import *

from meutils.oss.minio_oss import Minio  # minio_client

from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

from chatllm.utils.openai_utils import per_create
from chatllm.llmchain.document_loaders.file_loader import UnstructuredAPIFileLoader
from chatllm.llmchain.completions import chatglm_web, kimi

from enum import Enum
# from redis import Redis
from redis.asyncio import Redis

from openai import OpenAI, AsyncOpenAI
from openai._types import FileTypes
from openai.types.file_object import FileObject
from fastapi import APIRouter, File, UploadFile, Query, Form, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import Response, FileResponse, JSONResponse

router = APIRouter()

# file_info = {}  # or Redis(**os.getenv("REDIS_CLIENT_PARAMS", {}), decode_responses=True)  # redis_client_params
file_info = Redis()  # redis_client_params

kimi_client = AsyncOpenAI(
    api_key=os.getenv('MOONSHOT_API_KEY'),
    base_url=os.getenv('MOONSHOT_BASE_URL'),
)


class Purpose(str, Enum):
    file_upload = "file-upload"
    file_upload_glm = "file-upload-glm"

    file_extract = "file-extract"  # kimi glm
    file_extract_kimi = "file-extract-kimi"

    file_extract_plus = "file-extract-plus"  # 自研

    rag = "rag"
    file_structuring = "file_structuring"
    file_embedding = "file_embedding"

    assistants = "assistants"
    fine_tune = "fine-tune"


OPENAI_BUCKET = os.getenv('OPENAI_BUCKET', 'test')

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def go_to_baidu():
    return RedirectResponse("https://www.baidu.com")


@router.post("/files")  # 同名文件会被覆盖
async def upload_files(
    file: Union[UploadFile] = File(...),  # 文件链接
    purpose: Purpose = Form(...),
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    """
    todo: 存储redis
    """
    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")

    if purpose == Purpose.file_upload:  # 单纯的上传
        return await Minio().put_object_for_openai(file=file, purpose=purpose.value)

    # elif purpose == Purpose.file_extract_plus:
    #     content = await UnstructuredAPIFileLoader.load_for_openai(file)

    elif purpose == Purpose.file_extract:
        return await kimi_client.files.create(file=(file.filename, file.file), purpose=purpose.value)

    elif purpose == Purpose.file_extract_kimi:
        return kimi.Completions().file_extract(file=file)  # todo: 异步

    elif purpose == Purpose.file_upload_glm:
        return await chatglm_web.Completions().put_object_for_openai(file=file, purpose=purpose.value)

    elif purpose == Purpose.rag:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="暂不支持")


@router.get("/files/{file_id}/content")
async def get_files_content(
    file_id: str,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),

):
    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")

    async with Redis(decode_responses=True) as redis_client:
        content = await redis_client.get(file_id)

        if file_id.startswith("cn"):
            if content is None:
                response = await kimi_client.files.content(file_id=file_id)
                await kimi_client.files.delete(file_id)  # 删除文件
                content = response.text

        if content is None:
            url = f"https://f.chatllm.vip/{OPENAI_BUCKET}/{file_id}"
            content = await UnstructuredAPIFileLoader.load_for_openai(url)
            content = json.dumps(content, ensure_ascii=False)

            # response = await Minio().aget_object(OPENAI_BUCKET, file_id)
            # response = Minio().get_object(OPENAI_BUCKET, file_id)
            # content = response.read()
            # file = io.BytesIO(content)

            # content = file_info.get(file_id)  # redis缓存

        # await redis_client.set(file_id, content)  # 为啥抛错
        redis_client.set(file_id, content)  # 为啥抛错

    # 解析内容不支持 files.content(file_id).stream_to_file('xx.pdf')
    return Response(content=content, media_type="application/json")  # json.dumps(content, ensure_ascii=False)


@router.get("/files/{file_id}")
async def get_files(
    file_id: str,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")

    if file_id.startswith("cn"):  # kimi
        return await kimi_client.files.retrieve(file_id=file_id)

    # 映射 file_id
    # response = Minio().get_object(OPENAI_BUCKET, file_id)
    response = await Minio().aget_object(OPENAI_BUCKET, file_id)
    data = response.read()

    return FileObject(
        id=file_id,
        bytes=len(data),
        created_at=int(time.time()),
        filename=file_id,  # filename
        object='file',
        purpose='assistants',
        status='processed',
    )


@router.delete("/files/{file_id}")
async def delete_file(
    file_id: str,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")

    if file_id.startswith("cn"):  # kimi
        response = await kimi_client.files.delete(file_id=file_id)
        return response


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    VERSION_PREFIX = '/v1'

    app = App()
    app.include_router(router, VERSION_PREFIX)
    app.run(port=9000)
