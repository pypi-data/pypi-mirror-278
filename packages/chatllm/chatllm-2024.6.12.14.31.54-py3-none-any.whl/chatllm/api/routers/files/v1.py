#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : file_upload
# @Time         : 2024/5/31 15:25
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 增加计费

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
from fastapi.responses import Response, FileResponse, JSONResponse, RedirectResponse

router = APIRouter()


class Purpose(str, Enum):
    file_upload = "file-upload"  # glm
    file_upload_minio = "file_upload_minio"

    file_extract = "file-extract"  # kimi glm
    file_extract_kimi = "file-extract-kimi"

    file_extract_plus = "file-extract-plus"  # 自研

    rag = "rag"
    file_structuring = "file_structuring"
    file_embedding = "file_embedding"

    assistants = "assistants"
    fine_tune = "fine-tune"


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

    if purpose == Purpose.file_upload:
        return await chatglm_web.Completions().put_object_for_openai(file=file, purpose="file_upload")

    elif purpose == Purpose.file_upload_minio:  # 单纯的上传
        return await Minio().put_object_for_openai(file=file, purpose=purpose.value)

    # # elif purpose == Purpose.file_extract_plus:
    # #     content = await UnstructuredAPIFileLoader.load_for_openai(file)
    #
    # elif purpose == Purpose.file_extract:
    #     return await kimi_client.files.create(file=(file.filename, file.file), purpose=purpose.value)
    #
    # elif purpose == Purpose.file_extract_kimi:
    #     return kimi.Completions().file_extract(file=file)  # todo: 异步

    elif purpose == Purpose.rag:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="暂不支持")
