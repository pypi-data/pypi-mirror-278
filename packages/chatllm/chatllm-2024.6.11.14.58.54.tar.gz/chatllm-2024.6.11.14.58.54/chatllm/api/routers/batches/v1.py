#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : v1
# @Time         : 2024/5/31 13:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *
from meutils.llm.openai_utils import appu
from meutils.serving.fastapi.dependencies.auth import get_bearer_token, HTTPAuthorizationCredentials
from chatllm.schemas.openai_types import BatchRequest

from openai import OpenAI, AsyncOpenAI

from fastapi import APIRouter, File, UploadFile, Query, Form, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.responses import Response, FileResponse, JSONResponse, RedirectResponse

router = APIRouter()

zhipu_client = AsyncOpenAI(
    api_key=os.getenv('ZHIPU_API_KEY'),
    base_url=os.getenv('ZHIPU_BASE_URL'),
)


@router.post("/batches")
async def create_batch(
    request: BatchRequest,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token),
):
    logger.debug(request)

    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")

    request.endpoint = request.endpoint.replace("/v1/chat/completions", "/v4/chat/completions")
    batch_object = await zhipu_client.batches.create(**request.model_dump(), )

    # await appu("ppu-01", api_key)
    return batch_object


@router.get("/batches/{batch_id}")
async def retrieve_batch(
    batch_id: str,
    auth: Optional[HTTPAuthorizationCredentials] = Depends(get_bearer_token)
):
    api_key = auth and auth.credentials or None
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="认证失败")
    batch_object = await zhipu_client.batches.retrieve(batch_id)

    # await appu("ppu-001", api_key)
    return batch_object


# @router.get(
#     "/batches",
#     responses={
#         200: {"model": ListBatchesResponse, "description": "Batch listed successfully."},
#     },
#     tags=["Batch"],
#     summary="List your organization&#39;s batches.",
#     response_model_by_alias=True,
# )
# async def list_batches(
#     after: str = Query(None,
#                        description="A cursor for use in pagination. &#x60;after&#x60; is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with obj_foo, your subsequent call can include after&#x3D;obj_foo in order to fetch the next page of the list. ")
#     ,
#     limit: int = Query(20,
#                        description="A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 20. ")
#     ,
#     token_ApiKeyAuth: TokenModel = Security(
#         get_token_ApiKeyAuth
#     ),
# ) -> ListBatchesResponse:
#     ...
#
# @router.post(
#     "/batches/{batch_id}/cancel",
#     responses={
#         200: {"model": Batch, "description": "Batch is cancelling. Returns the cancelling batch&#39;s details."},
#     },
#     tags=["Batch"],
#     summary="Cancels an in-progress batch.",
#     response_model_by_alias=True,
# )
# async def cancel_batch(
#     batch_id: str = Path(..., description="The ID of the batch to cancel.")
#     ,
#     token_ApiKeyAuth: TokenModel = Security(
#         get_token_ApiKeyAuth
#     ),
# ) -> Batch:
#     ...

if __name__ == '__main__':
    from meutils.serving.fastapi import App

    VERSION_PREFIX = '/v1'

    app = App()
    app.include_router(router, VERSION_PREFIX)
    app.run(port=8000)
