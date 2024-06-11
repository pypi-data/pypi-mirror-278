#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : chatglm_web
# @Time         : 2024/3/11 18:52
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm 🧩 🔨[🔨](…….)
# @Description  : https://github.com/ikechan8370/chatgpt-plugin/blob/32af7b9a74fdfbd329f5977c6e3fb5b3928ed0f1/client/ChatGLM4Client.js#L6
import shortuuid

from meutils.pipe import *
from meutils.notice.feishu import send_message

from chatllm.schemas import chatglm_types
from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest
from chatllm.utils.openai_utils import openai_response2sse
from fastapi import UploadFile
from openai.types.file_object import FileObject


class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')
        self.access_token = self.get_access_token(self.api_key)

        self.httpx_client = httpx.Client(headers=self.headers, follow_redirects=True)
        self.httpx_aclient = httpx.AsyncClient(headers=self.headers, follow_redirects=True)

    # def create(self):
    #
    #     self.httpx_client.post(url, json={})

    def create(self, request: ChatCompletionRequest):
        request = self.do_request(request)

        url = "https://chatglm.cn/chatglm/backend-api/assistant/stream"
        payload = isinstance(request, dict) and request or request.model_dump()
        # response = self.httpx_client.post(url=url, json=payload)
        response: httpx.Response
        with self.httpx_client.stream("POST", url=url, json=payload, timeout=200) as response:

            content = ""
            for chunk in response.iter_lines():
                for chat_completion_chunk in self.do_chunk(chunk):
                    _ = chat_completion_chunk.choices[0].delta.content
                    chat_completion_chunk.choices[0].delta.content = _.split(content)[-1] if content else _
                    yield chat_completion_chunk
                    content = _

    async def acreate(self, request: Union[dict, ChatCompletionRequest]):
        request = self.do_request(request)

        url = "https://chatglm.cn/chatglm/backend-api/assistant/stream"
        payload = isinstance(request, dict) and request or request.model_dump()
        # response = self.httpx_client.post(url=url, json=payload)
        response: httpx.Response
        async with self.httpx_aclient.stream("POST", url=url, json=payload, timeout=200) as response:
            content = ""
            async for chunk in response.aiter_lines():
                for chat_completion_chunk in self.do_chunk(chunk):
                    _ = chat_completion_chunk.choices[0].delta.content
                    chat_completion_chunk.choices[0].delta.content = _.split(content)[-1] if content else _
                    yield chat_completion_chunk
                    content = _

    def create_sse(self, request: ChatCompletionRequest):
        if request.stream:
            return openai_response2sse(self.acreate(request), redirect_model=request.model)
        else:
            _chat_completion = chat_completion.model_copy(deep=True)
            _chat_completion.usage.prompt_tokens = len(request.messages[-1]["content"])
            for i in self.create(request):  # todo: 异步
                _chat_completion.choices[0].message.content += i.choices[0].delta.content

            return openai_response2sse(_chat_completion, redirect_model=request.model)

    def do_chunk(self, chunk):

        if chunk := chunk.strip().strip("event:message\ndata: ").strip():

            # logger.debug(chunk)

            chunk = chatglm_types.Data.model_validate_json(chunk)
            content = chunk.parts and chunk.parts[0].markdown_data
            if content:
                # logger.debug(content)
                # yield content
                chat_completion_chunk.choices[0].delta.content = content
                yield chat_completion_chunk

            if chunk.status == 'finish':
                _ = chat_completion_chunk.model_copy(deep=True)
                _.choices[0].delta.content = ""
                _.choices[0].finish_reason = "stop"  # 特殊
                yield _
                return

    def do_request(self, request: ChatCompletionRequest):

        history = request.messages[:-1]
        history = history and f"""参考系统历史对话，以聊天的语气回答问题：\n```json\n{json.dumps(history, ensure_ascii=False, indent=4)}\n```"""  # todo: 优化

        question = request.messages[-1]["content"]
        if isinstance(question, list):  # todo: 兼容多模态
            # 文件  {"type": "image_url", "image_url": {"url": image_url1}}
            # {
            #     "type": "http://ai.chatfire.cn/files/document/绩效面谈表-模版-nine-1710139239100-nine-66b3829d5.pdf text"
            # }

            send_message(request.messages)

        request.messages = [
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': f"""{history}\n\n问题：{question}""" if history else question
                    }
                ]
            }
        ]

        # logger.debug(request)

        return request

    def file_extract(self):
        """
        {
          "message": "success",
          "result": {
            "file_id": "chatglm4/f960da34-0041-4662-96e7-791ea455618a.png",
            "file_name": "8E8F00E40FED35D93339FF66691017CC.png",
            "file_size": 0,
            "file_url": "https://sfile.chatglm.cn/chatglm4/f960da34-0041-4662-96e7-791ea455618a.png",
            "height": 1024,
            "width": 1024
          },
          "status": 0
        }
        :return:
        """
        url = "https://chatglm.cn/chatglm/backend-api/assistant/file_upload"
        pass

    @property
    def headers(self):
        return {
            'Authorization': f"Bearer {self.access_token}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

    @staticmethod
    @ttl_cache(3600 * 2)
    def get_access_token(refresh_token=None):  # 设计重试
        refresh_token = refresh_token or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMDE0OTU3OCwianRpIjoiYmQ3YWI2ZDItNWViNS00YmVmLTlmMWMtYzU5NTMwM2IyN2ZkIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIzNmE4NmM1Yzc2Y2Q0MTcyYTE5NGYxMjQwZTgyMmIwOSIsIm5iZiI6MTcxMDE0OTU3OCwiZXhwIjoxNzI1NzAxNTc4LCJ1aWQiOiI2NDRhM2QwY2JhMjU4NWU5MDQ2MDM5ZGIiLCJ1cGxhdGZvcm0iOiIiLCJyb2xlcyI6WyJ1bmF1dGhlZF91c2VyIl19.gN8ci_OO8Pp0t3wZ3v1lG2X1xoLgGushf3fkm5pRl0M"

        headers = {
            'Authorization': f"Bearer {refresh_token}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        url = "https://chatglm.cn/chatglm/backend-api/v1/user/refresh"
        response = httpx.post(url, headers=headers)

        # logger.debug(refresh_token)
        # logger.debug(response.text)
        # logger.debug(response.status_code)

        if response.status_code != 200:
            send_message(f"GLM refresh_token:\n\n{response.text}\n\n{refresh_token}", title="GLM")
            response.raise_for_status()

        # refresh_token = response.get("refresh_token") # 是否去更新
        return response.json().get("result", {}).get("accessToken")

    async def put_object_for_openai(
        self,
        file: Union[bytes, str, Path, UploadFile],
        purpose: str = "chatpdf_file_upload",  # file_upload
        filename: Optional[str] = None,
    ):  # filename => file url 预览https://sfile.chatglm.cn/doc_mobile/fdfeeea2-2721-445a-a8f6-b70a7972c1da.pdf
        if isinstance(file, bytes):
            filename = filename or f"{shortuuid.random()}.png"

        elif isinstance(file, (str, Path)) and Path(file).exists():
            filename = Path(file).name
            file = Path(file).read_bytes()
        else:
            filename = file.filename or file.file.name
            file = file.file

        # base_url = "https://chatglm.cn/chatglm/backend-api/v1/chatpdf_file_upload"
        #
        # base_url = "https://chatglm.cn/chatglm/backend-api/assistant/file_upload"

        # try:
        # 通用
        base_url = "https://chatglm.cn/chatglm/backend-api"
        url = "/v1/chatpdf_file_upload" if purpose == "chatpdf_file_upload" else "/assistant/file_upload"

        payload = {"file": (filename, file)}
        try:
            async with httpx.AsyncClient(headers=self.headers, base_url=base_url, timeout=60) as client:
                response = await client.post(url=url, files=payload)
                if response.status_code != 200:
                    response.raise_for_status()

                # logger.debug(response.json())
                # {'message': '内容已超过对话长度62.25%，请删减部分文件', 'result': [], 'status': 2}

                result = response.json().get("result") or {}

                return FileObject.construct(
                    id=result.get("file_id"),
                    bytes=result.get("content_length"),
                    created_at=int(time.time()),
                    filename=result.get("file_url"),  # result.get("file_name")
                    object='file',
                    purpose=purpose,
                    status='processed' if result else "error",
                    status_details=result
                )

        except Exception as e:
            return str(e)  # todo


# {
#     "message": "success",
#     "result": {
#         "content_length": 37910,
#         "content_raw_length": 37910,
#         "conversation_id": "65f43c951f86227d538333d9",
#         "file_url": "https://sfile.chatglm.cn/doc_mobile/fdfeeea2-2721-445a-a8f6-b70a7972c1da.pdf",
#         "prompt": "东北证券股份有限公司合规手册（东证合规发〔2023〕22号 20231228）.pdf",
#         "questions": [
#             "东北证券合规手册的主要内容包括哪些章节？",
#             "东北证券合规手册对工作人员有哪些具体要求？",
#             "东北证券合规手册对各类业务有哪些合规底线要求？"
#         ],
#         "severity_type": 0,
#         "summary": "这份合规手册来自东北证券股份有限公司，旨在进一步落实“合规、诚信、专业、稳健”的行业文化要求，规范公司各单位及工作人员执业行为，有效防范合规风险，促进全体工作人员形成“全员合规、合规从管理层做起、合规创造价值、合规是公司生存基础”的合规理念和“十个坚持、十个反对”的荣辱观。合规手册包括合规管理、工作人员执业行为规范、公司各类业务的合规底线以及需要遵循的其他规定等部分。此外，该手册还强调了公司合规管理的目标、原则和基本要求，包括充分了解客户信息、合理划分客户类别和产品风险等级、持续督促客户规范证券发行行为等。同时，该手册还明确规定了各类业务的合规底线，包括证券经纪业务、投资银行业务、证券自营及衍生品业务等。"
#     },
#     "status": 0
# }

# {
#     "message": "success",
#     "result": {
#         "content_length": 17908,
#         "content_raw_length": 17908,
#         "file_id": "chatglm4/82834747-0fcf-4ecb-94b0-92e5e749798b.docx",
#         "file_name": "中华人民共和国公司法（2023年修订 20231229 20240701）.docx",
#         "file_size": 0,
#         "file_url": "https://sfile.chatglm.cn/chatglm4/82834747-0fcf-4ecb-94b0-92e5e749798b.docx",
#         "questions": [],
#         "questions_usage": {},
#         "summary": "",
#         "summary_usage": {}
#     },
#     "status": 0
# }

if __name__ == '__main__':
    # print(Completions.get_access_token())

    # data = {
    #     "assistant_id": "65940acff94777010aa6b796",
    #     "conversation_id": "",
    #     # "conversation_id": "",
    #     # "meta_data": {
    #     #     "is_test": False,
    #     #     "input_question_type": "xxxx",
    #     #     "channel": "",
    #     #     "draft_id": ""
    #     # },
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": [
    #                 {
    #                     "type": "text",
    #                     # "text": "你是一个资深民商事律师，请你运用联网功能，帮我解决以下问题：\n压岁钱的所有权归谁，父母是否有权支配孩子压岁钱？\n请帮我写出相关法条和判例。",
    #                     # "text": "南京今天天气"
    #                     # "text": "画只猫"
    #                     # "text": "1+2"
    #                     "text": "总结一下 http://www.weather.com.cn/weather/101190101.shtml"
    #
    #                 }
    #             ]
    #         }
    #
    #     ]
    # }

    # data = {
    #     # "assistant_id": "65940acff94777010aa6b796",
    #     "assistant_id": "65f41c8a9c0ebbcbe28bb9c1",  # 智能体
    #     # "conversation_id": "65f41fe143c80c1f80b55150",
    #     # "conversation_id": "",
    #     # "meta_data": {
    #     #     "is_test": False,
    #     #     "input_question_type": "xxxx",
    #     #     "channel": "",
    #     #     "draft_id": ""
    #     # },
    #     "messages": [
    #         {
    #             "role": "user",
    #             "content": "从业人员可以炒股吗"
    #         }
    #
    #     ]
    # }
    #
    # for i in Completions().create(ChatCompletionRequest(**data)):
    #     print(i.choices[0].delta.content, end="")
    #     # pass

    _ = Completions().put_object_for_openai(Path("/Users/betterme/PycharmProjects/AI/QR.png").read_bytes(), "")  # 上传文件

    print(arun(_, debug=True))
    print(_)
    pass
