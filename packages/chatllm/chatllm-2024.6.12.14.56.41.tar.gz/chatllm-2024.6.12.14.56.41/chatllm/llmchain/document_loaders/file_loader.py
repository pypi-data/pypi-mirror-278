#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : file_loader
# @Time         : 2024/3/15 16:48
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *
from langchain_community.document_loaders import UnstructuredAPIFileLoader as _UnstructuredAPIFileLoader
from fastapi import APIRouter, File, UploadFile, Query, Form, BackgroundTasks, Depends, HTTPException, Request, status


class MetaData(BaseModel):
    source: Optional[str] = None

    languages: Optional[Any] = []
    page_number: Optional[int] = None
    filename: Optional[str] = None
    filetype: Optional[str] = None
    parent_id: Optional[str] = None
    category: Optional[str] = None

    type: str = 'Document'


class UnstructuredAPIFileLoader(_UnstructuredAPIFileLoader):
    """
    加缓存 异步
    """

    def __init__(
        self,
        file_path: Optional[Union[str, List[str]]] = None,
        mode: Literal["single", "elements", "paged"] = "paged",
        **kwargs
    ):
        super().__init__(file_path, mode=mode, **kwargs)
        base_url = os.getenv("UNSTRUCTURED_BASE_URL", self.url).rstrip('/')
        # url: str = "https://api.unstructured.io/general/v0/general",

        self.url = f"{base_url}/general/v0/general"
        self.api_key = os.getenv("UNSTRUCTURED_API_KEY", "")
        # todo: 重写

    @classmethod
    async def load_for_openai(cls, file: Union[str, UploadFile]):
        """
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        _text_splitter: TextSplitter = RecursiveCharacterTextSplitter()
        _text_splitter.split_documents(docs)

        :return:
        """
        if isinstance(file, str) and file.startswith("http"):
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.get(url=file)
                file = UploadFile(
                    file=io.BytesIO(response.content),
                    filename=Path(file).name,
                    size=len(response.content),
                    headers=response.headers,  # content_type
                )

        # logger.info(f"file: {file}")

        object = cls(file=file.file, strategy="fast", metadata_filename=file.filename, mode='single')  # todo: 同步转异步
        # object.load_and_split()
        docs = object.load()

        return docs and docs[0].dict() or "{}"  # todo:会不会不止一个文档


if __name__ == '__main__':
    loader = UnstructuredAPIFileLoader(
        # file_path="/Users/betterme/PycharmProjects/AI/ChatLLM/examples/openaisdk/new.pdf",

        # file_path=None,
        file=open("/Users/betterme/PycharmProjects/AI/ChatLLM/data/不存在的骑士01.pdf", 'rb'),
        metadata_filename="new.pdf",
    )

    with timer("解析"):
        print(loader.load_and_split())

    # with timer("解析"):
    #     _ = UnstructuredAPIFileLoader.load_for_openai(
    #         # "https://sfile.chatglm.cn/chatglm4/82834747-0fcf-4ecb-94b0-92e5e749798b.docx"
    #         "https://f.chatllm.vip/test/3MvAKgEoBrBdPgWsQSdTB8.pdf"
    #     )
    #     docs = arun(_)
    #     # print(docs)
