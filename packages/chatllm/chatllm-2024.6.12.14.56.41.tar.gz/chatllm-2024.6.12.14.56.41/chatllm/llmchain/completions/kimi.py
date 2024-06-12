#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kimi
# @Time         : 2024/2/29 15:09
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/search?q=https%3A%2F%2Fkimi.moonshot.cn%2Fapi%2Fchat&type=code

from meutils.pipe import *
from meutils.notice.feishu import send_message
from meutils.str_utils.regular_expression import parse_url

from chatllm.schemas.kimi_types import KimiData
from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.utils.openai_utils import openai_response2sse

from fastapi import UploadFile
from openai.types.file_object import FileObject


class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')  # refresh_token
        self.access_token = client_params.get("access_token") or self.get_access_token(self.api_key)  # access_token

        self.httpx_client = httpx.Client(headers=self.headers, follow_redirects=True)
        self.httpx_aclient = httpx.AsyncClient(headers=self.headers, follow_redirects=True)

    def create(self, request: ChatCompletionRequest):
        request = self.do_request(request)

        url = f"https://kimi.moonshot.cn/api/chat/{self.chat_id}/completion/stream"

        payload = request.model_dump()
        # response = self.httpx_client.post(url=url, json=payload)
        response: httpx.Response
        with self.httpx_client.stream("POST", url=url, json=payload) as response:
            for line in response.iter_lines():
                yield from self.do_chunk(line)

    async def acreate(self, request: ChatCompletionRequest):
        request = self.do_request(request)

        # chat_id =request.conversation_id or self.chat_id # 会话失败还得重新建

        url = f"https://kimi.moonshot.cn/api/chat/{self.chat_id}/completion/stream"

        payload = request.model_dump()
        # response = self.httpx_client.post(url=url, json=payload)
        response: httpx.Response
        async with self.httpx_aclient.stream("POST", url=url, json=payload) as response:
            async for line in response.aiter_lines():
                for chunk in self.do_chunk(line):
                    yield chunk

                    # 多输出几行就可以替换掉kimi【水印】
                    # 我是Kimi，由月之暗面科技有限公司开发的人工智能助手。我在这里为您提供帮助，回答问题，并协助您处理各种信息和任务。如果您有任何问题或需要帮助，请随时告诉我！

    def create_sse(self, request: ChatCompletionRequest):
        if request.stream:
            return openai_response2sse(self.acreate(request), redirect_model=request.model)
        else:
            _chat_completion = chat_completion.model_copy(deep=True)
            _chat_completion.usage.prompt_tokens = len(request.messages[-1]["content"])
            for i in self.create(request):
                _chat_completion.choices[0].message.content += i.choices[0].delta.content

            return openai_response2sse(_chat_completion, redirect_model=request.model)

    def do_request(self, request: ChatCompletionRequest):

        history = request.messages[:-1]
        history = history and f"""可参考系统历史对话回答问题：\n```json\n{json.dumps(history, ensure_ascii=False, indent=4)}\n```"""  # todo: 优化
        # history = history and f"""History:\n```json\n{json.dumps(history, ensure_ascii=False, indent=4)}\n```"""

        question = request.messages[-1]["content"]
        if isinstance(question, list):
            # 文件  {"type": "image_url", "image_url": {"url": image_url1}}
            # {
            #     "type": "http://ai.chatfire.cn/files/document/绩效面谈表-模版-nine-1710139239100-nine-66b3829d5.pdf text"
            # }

            send_message(request.messages)

        # 链接转换
        if not request.model.startswith(("moonshot",)):  # moonshot不支持链接
            question = self._url2content(question) or question

        request.messages = [
            {
                'role': 'user',
                'content': f"""{history}\n\nQuery: {question}""" if history else question
            }
        ]

        return request

    def do_chunk(self, line):

        if line := line.strip().strip('data: '):

            logger.debug(line)

            kimi_data = KimiData.model_validate_json(line)

            for chunk in self.search_plus(kimi_data):
                yield chunk

            if kimi_data.event == 'cmpl':
                chat_completion_chunk.choices[0].delta.content = kimi_data.content
                yield chat_completion_chunk

            if kimi_data.event == 'all_done':
                _ = chat_completion_chunk.model_copy(deep=True)
                _.choices[0].delta.content = ""
                _.choices[0].finish_reason = "stop"  # 特殊
                yield _
                return

    def _url2content(self, content) -> Union[bool, str]:
        urls = parse_url(content)
        if not urls: return False

        for i, url in enumerate(urls):
            _url = f""" <url id="{i}" type="url" status="" title="" wc="">{url}</url> """
            content = content.replace(url, _url)

        return content

    def search_plus(self, kimi_data: KimiData):
        if kimi_data.event == 'search_plus':
            if kimi_data.msg.get("type") == "start":  # start_res
                chat_completion_chunk.choices[0].delta.content = "---\n🔎 开始搜索 🚀\n"
                yield chat_completion_chunk
            if kimi_data.msg.get("type") == "get_res":
                title = kimi_data.msg.get("title")
                url = kimi_data.msg.get("url")
                chat_completion_chunk.choices[0].delta.content = f"""- 🔗 [{title}]({url})\n"""
                yield chat_completion_chunk

            if kimi_data.msg.get("type") == "answer":
                chat_completion_chunk.choices[0].delta.content = f"""---\n\n"""
                yield chat_completion_chunk

    @property
    def chat_id(self):
        url = "https://kimi.moonshot.cn/api/chat"
        payload = {"name": str(datetime.datetime.now()), "is_example": False}
        response = self.httpx_client.post(url, json=payload)

        if response.status_code != 200:
            send_message(f"Kimi access_token:\n\n{response.text}", title="Kimi")
            response.raise_for_status()

        return response.json().get('id')

    @property
    def headers(self):
        return {
            'Authorization': f"Bearer {self.access_token}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

    @staticmethod
    @ttl_cache(600)
    def get_access_token(refresh_token=None):  # 设计重试
        refresh_token = refresh_token or os.getenv(
            "KIMI_REFRESH_TOKEN") or "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxNjk2NzcxNiwiaWF0IjoxNzA5MTkxNzE2LCJqdGkiOiJjbmczNDkybG5sOTB2cnIzY21qZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJja2kwOTRiM2Flc2xnbGo2Zm8zMCIsInNwYWNlX2lkIjoiY2tpMDk0YjNhZXNsZ2xqNmZvMmciLCJhYnN0cmFjdF91c2VyX2lkIjoiY2tpMDk0YjNhZXNsZ2xqNmZvMzAifQ.S2T2c3rfFaQmyYMURLpgpmp2O1Voojy3b6-qoP0Hnrlvk6Y8Zxn2ku6U0ZEMW48KbG-fqaYlbF8lWUfsuSVSEQ"

        headers = {
            'Authorization': f"Bearer {refresh_token}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        url = "https://kimi.moonshot.cn/api/auth/token/refresh"
        response = httpx.get(url, headers=headers, verify=False)

        # logger.debug(refresh_token)
        # logger.debug(response.text)
        # logger.debug(response.status_code)

        if response.status_code != 200:
            send_message(f"Kimi refresh_token:\n\n{response.text}\n\n{refresh_token}", title="Kimi")
            response.raise_for_status()

        # refresh_token = response.get("refresh_token") # 是否去更新
        return response.json().get("access_token")

    def file_extract(self, file: Union[str, Path, UploadFile]):

        if isinstance(file, str) and Path(file).exists():
            filename = Path(file).name
            file = Path(file).read_bytes()
        else:
            filename = file.filename or file.file.name
            file = file.file

        url = "https://kimi.moonshot.cn/api/pre-sign-url"
        payload = {"action": "file", "name": filename}
        pre_sign_response = self.httpx_client.post(url, json=payload).json()

        # logger.debug(pre_sign_response)

        url = pre_sign_response.get('url')
        object_name = pre_sign_response.get("object_name")

        # 上传文件
        files = {'file': file}
        self.httpx_client.put(url, files=files)

        # 获取文件id
        url = "https://kimi.moonshot.cn/api/file"
        payload = {"type": "file", "name": filename, "object_name": object_name}
        file_response = self.httpx_client.post(url, json=payload, headers=self.headers).json()

        # logger.debug(file_response)
        # {
        #     "id": "cnrtn82lnl9f8h6k6eqg",
        #     "name": "东北证券股份有限公司合规手册（东证合规发〔2023〕22号 20231228）.pdf",
        #     "parent_path": "",
        #     "type": "file",
        #     "status": "initialized",
        #     "presigned_url": "https://prod-chat-kimi.tos-s3-cn-beijing.volces.com/prod-chat-kimi/cki094b3aeslglj6fo2g/2024-03-18/cnrtn7998onq6ckol4jg/%E4%B8%9C%E5%8C%97%E8%AF%81%E5%88%B8%E8%82%A1%E4%BB%BD%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%E5%90%88%E8%A7%84%E6%89%8B%E5%86%8C%EF%BC%88%E4%B8%9C%E8%AF%81%E5%90%88%E8%A7%84%E5%8F%91%E3%80%942023%E3%80%9522%E5%8F%B7%2020231228%EF%BC%89.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256\u0026X-Amz-Credential=AKLTYTJlNjgwMjY2ZDBkNDFiYmI5YWNiZDBlZmFmYjIzZTA%2F20240318%2Fcn-beijing%2Fs3%2Faws4_request\u0026X-Amz-Date=20240318T061352Z\u0026X-Amz-Expires=3600\u0026X-Amz-SignedHeaders=host\u0026X-Amz-Signature=95041dfc608a81e07fe0b91d6bb44668112d057b6b6313dde6d23ea1e76c9b77",
        #     "text_presigned_url": "https://prod-chat-kimi.tos-s3-cn-beijing.volces.com/prod-chat-kimi/cki094b3aeslglj6fo2g/2024-03-18/cnrtn82lnl9f8h6k6eq0/?X-Amz-Algorithm=AWS4-HMAC-SHA256\u0026X-Amz-Credential=AKLTYTJlNjgwMjY2ZDBkNDFiYmI5YWNiZDBlZmFmYjIzZTA%2F20240318%2Fcn-beijing%2Fs3%2Faws4_request\u0026X-Amz-Date=20240318T061352Z\u0026X-Amz-Expires=3600\u0026X-Amz-SignedHeaders=host\u0026X-Amz-Signature=c1157fd8a0b65864a89480bb9e743d48004705126a7c04c24c0e2abc15131773",
        #     "uploaded_at": "2024-03-18T06:13:49Z",
        #     "created_at": "2024-03-18T14:13:52.036471136+08:00",
        #     "updated_at": "2024-03-18T14:13:52.036471136+08:00"
        # }

        file_id = file_response.get("id")

        # 解析文件
        url = "https://kimi.moonshot.cn/api/file/parse_process"
        payload = {"ids": [file_id]}
        resp = self.httpx_client.post(url, json=payload, headers=self.headers, timeout=180).text.strip('data: ')
        resp = json.loads(resp)
        resp['file_info'].update(file_response)

        logger.debug(resp)

        status = resp.get("status") == "parsed" and "processed" or "error"

        file_object = FileObject(
            id=file_id,
            bytes=resp['file_info']['size'],
            created_at=int(time.time()),
            filename=filename,
            object='file',
            purpose="assistants",
            status=status,
            status_details=str(resp)
        )

        return file_object

    def file_upload(self, file: Union[str, UploadFile]):
        return self.file_extract(file)


# 2024-03-04 09:29:24.815 | DEBUG    | __main__:f:186 - {'ids': ['cnii7t4udu62fbesjteg']}
# data: {"event":"resp","file_info":{"id":"cnii7t4udu62fbesjteg","name":"å­å­åµæ³.pdf","type":"file","content_type":"pdf","status":"parsed","size":607093,"token_size":91753,"failed_reason":""},"id":"cnii7t4udu62fbesjteg","status":"parsed"}


# def do_refresh_token(refresh_token):
#     headers = {
#         'Authorization': f'Bearer {refresh_token}'
#     }
#
#     response = requests.get("https://kimi.moonshot.cn/api/auth/token/refresh", headers=headers)
#     print(response.status_code)
#
#     return response.json()  # {"access_token": "", "refresh_token": ""} {'error_type': 'auth.token.invalid', 'message': '您的授权已过期，请重新登录'}
#
#
# refresh_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxNjk2NzcxNiwiaWF0IjoxNzA5MTkxNzE2LCJqdGkiOiJjbmczNDkybG5sOTB2cnIzY21qZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJja2kwOTRiM2Flc2xnbGo2Zm8zMCIsInNwYWNlX2lkIjoiY2tpMDk0YjNhZXNsZ2xqNmZvMmciLCJhYnN0cmFjdF91c2VyX2lkIjoiY2tpMDk0YjNhZXNsZ2xqNmZvMzAifQ.S2T2c3rfFaQmyYMURLpgpmp2O1Voojy3b6-qoP0Hnrlvk6Y8Zxn2ku6U0ZEMW48KbG-fqaYlbF8lWUfsuSVSEQ"
#
# with timer("监控token过期时间"):
#     for i in tqdm(range(1000)):
#         response = do_refresh_token(refresh_token)
#         refresh_token = response.get("refresh_token")
#         access_token = response.get("access_token")
#         headers = {
#             'authorization': f'Bearer {access_token}'
#         }
#         response = requests.post(
#             "https://kimi.moonshot.cn/api/chat/cng35i6cp7f94p55g2u0/completion/stream",
#             json={'messages': [{'role': 'user', 'content': '1+1'}]},
#             headers=headers,
#
#         )
#         response.encoding = 'utf8'
#
#         logger.debug(response.text)
#
#         if not refresh_token:
#             break
#         time.sleep(60)


if __name__ == '__main__':
    # print(Completions.get_access_token())
    # print(Completions().access_token)

    # print(Completions().chat_id)
    t = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcwOTgwMDIxMCwiaWF0IjoxNzA5Nzk5MzEwLCJqdGkiOiJjbmtuZjNocmRpamFpbGlkNGNqZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNraTA5NGIzYWVzbGdsajZmbzMwIiwic3BhY2VfaWQiOiJja2kwOTRiM2Flc2xnbGo2Zm8yZyIsImFic3RyYWN0X3VzZXJfaWQiOiJja2kwOTRiM2Flc2xnbGo2Zm8zMCJ9.fm5Hd16J3DNtmRT4zctcKrIvojEcByORFfHm2OziddOMF1dL5nqX3U9skERvF-q-QlpSpMSm8SDRVLXde1Balw"
    c = Completions(access_token=t)
    c = Completions()

    # async def f(x):
    #     _ = c.create(
    #         ChatCompletionRequest(
    #             messages=[
    #                 # {'role': 'user', 'name': '_resource', 'content': "你现在扮演的角色是GPT请牢记"},
    #                 {'role': 'user', 'content': '1+1'},  # 不能有系统信息
    #                 # {'role': 'user', 'content': '总结这篇文章 https://f.chatllm.vip/rag-dev/trento2013.pdf'},
    #                 # {'role': 'user', 'content': '总结这篇文章'},
    #
    #             ],
    #             # file_ids=['cnijpe6cp7f0sq79ahtg']
    #             # file_ids=['cnimvq03r076lsmj7ohg']
    #         )
    #     )
    #
    #     _ = c.acreate(
    #         ChatCompletionRequest(
    #             messages=[
    #                 {'role': 'user', 'content': '1+1'},  # 不能有系统信息
    #
    #             ],
    #
    #         )
    #     )
    #     s = ""
    #     async for i in _:
    #         s += i.choices[0].delta.content
    #         print(i.choices[0].delta.content, end='')
    #
    #     chat_completion.choices[0].message.content = s
    #     return chat_completion
    #
    #
    # print(arun(f('')))

    # with timer("过期时间"):
    #     while 1:
    #
    #         try:
    #
    #             f('')
    #
    #             time.sleep(10)
    #
    #         except Exception as e:
    #             print(e)
    #             break

    # range(10) | xThreadPoolExecutor(f, 10) | xlist

    # _ = Completions().acreate(
    #     ChatCompletionRequest(messages=[{'role': 'user', 'content': '今天南京天气'}]))
    #
    # # async def main():
    # #     async for i in _:
    # #         yield i
    # print(type(_))
    # for i in async2sync_generator(_):
    #     print(i)

    print(Completions().file_extract('/Users/betterme/PycharmProjects/AI/ChatLLM/data/孙子兵法.pdf'))
