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
from meutils.db.redis_db import redis_aclient  # minio_client
from meutils.llm.openai_utils import appu

from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials

# from chatllm.llmchain.document_loaders.file_loader import UnstructuredAPIFileLoader
from chatllm.llmchain.completions import chatglm_web

from enum import Enum

from openai import OpenAI, AsyncOpenAI
from openai._types import FileTypes
from openai.types.file_object import FileObject
from fastapi import APIRouter, File, UploadFile, Query, Form, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import Response, FileResponse, JSONResponse

router = APIRouter()

kimi_client = AsyncOpenAI(
    api_key=os.getenv('MOONSHOT_API_KEY'),
    base_url=os.getenv('MOONSHOT_BASE_URL'),
)

zhipu_client = AsyncOpenAI(
    api_key=os.getenv('ZHIPU_API_KEY'),
    base_url=os.getenv('ZHIPU_BASE_URL'),
)


class Purpose(str, Enum):
    file_upload = "file-upload"
    file_upload_minio = "file-upload-minio"

    # file_upload_glm = "file-upload-glm"
    file_upload_chatpdf = "file-upload-chatpdf"

    file_extract = "file-extract"  # kimi glm
    # file_extract_kimi = "file-extract-kimi"
    #
    # file_extract_plus = "file-extract-plus"  # 自研
    #
    # rag = "rag"
    # file_structuring = "file_structuring"
    # file_embedding = "file_embedding"
    #
    # assistants = "assistants"
    # fine_tune = "fine-tune"
    batch = "batch"


OPENAI_BUCKET = os.getenv('OPENAI_BUCKET', 'files')


@router.post("/files")  # 同名文件会被覆盖
async def upload_files(
    file: Union[UploadFile] = File(...),  # 文件链接
    purpose: Purpose = Form(...),
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")

    if purpose == Purpose.file_upload:  # 单纯的上传
        try:
            file_object = await chatglm_web.Completions().put_object_for_openai(file=file, purpose="file-upload")

            await appu("ppu-001", api_key)
            return file_object
        except Exception as e:
            logger.error(e)

            file_object = await Minio().put_object_for_openai(file=file, purpose=purpose.value,
                                                              bucket_name=OPENAI_BUCKET)
            await appu("ppu-001", api_key)
            return file_object

    elif purpose == Purpose.file_upload_minio:
        file_object = await Minio().put_object_for_openai(file=file, purpose=purpose.value,
                                                          bucket_name=OPENAI_BUCKET)
        await appu("ppu-001", api_key)
        return file_object


    elif purpose == Purpose.batch:
        if not file.filename.endswith('jsonl'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={'error': {'code': '1622', 'message': f'文件内容异常:文件名{file.filename}扩展名只能为jsonl'}}
            )

        file_object = await zhipu_client.files.create(file=(file.filename, file.file), purpose="batch")
        await appu("ppu-01", api_key)
        return file_object

    # elif purpose == Purpose.file_extract_plus:
    #     content = await UnstructuredAPIFileLoader.load_for_openai(file)

    elif purpose == Purpose.file_extract:
        file_object = await kimi_client.files.create(file=(file.filename, file.file), purpose=purpose.value)

        await appu("ppu-01", api_key)
        return file_object

    # elif purpose == Purpose.file_extract_kimi:
    #     await appu("ppu-01", api_key)
    #     return await kimi_client.files.create(file=(file.filename, file.file), purpose=purpose.value)

    elif purpose == Purpose.file_upload_chatpdf:
        file_object = await chatglm_web.Completions().put_object_for_openai(file=file, purpose="chatpdf-file-upload")

        await appu("ppu-01", api_key)
        return file_object

    # elif purpose == Purpose.rag:
    #     raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="暂不支持")


@router.get("/files/{file_id}/content")
async def get_files_content(
    file_id: str,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),

):
    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")

    # 缓存
    content = await redis_aclient.get(file_id)

    # kimi
    if len(file_id) == 20:  # cpeni8onsmmqhvjjv5p0 好像是c开头，先用长度判断
        if content is None:
            response = await kimi_client.files.content(file_id=file_id)
            content = response.text
            # 缓存
            await redis_aclient.set(file_id, content, ex=3600 * 24 * 180)  # 180天
            await kimi_client.files.delete(file_id)  # 删除文件

    # if content is None:
    #     url = f"https://f.chatllm.vip/{OPENAI_BUCKET}/{file_id}"
    #     content = await UnstructuredAPIFileLoader.load_for_openai(url)
    #     content = json.dumps(content, ensure_ascii=False)
    #
    #     # response = await Minio().aget_object(OPENAI_BUCKET, file_id)
    #     # response = Minio().get_object(OPENAI_BUCKET, file_id)
    #     # content = response.read()
    #     # file = io.BytesIO(content)

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
