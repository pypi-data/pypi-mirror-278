#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : stepchat
# @Time         : 2024/3/26 11:28
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *
from meutils.notice.feishu import send_message

from chatllm.schemas.kimi_types import KimiData
from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.utils.openai_utils import openai_response2sse

"https://stepchat.cn/api/proto.chat.v1.ChatMessageService/SendMessageStream"
"https://stepchat.cn/api/proto.chat.v1.ChatService/GenerateChatName"


class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')  # refresh_token
        self.access_token = self.get_access_token()

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

    def get_access_token(self):
        url = "https://stepchat.cn/passport/proto.api.passport.v1.PassportService/RegisterDevice"

        response = httpx.post(url=url, json={}, headers=self.headers)

        logger.debug(response.text)
        return response.json().get('accessToken', {}).get('raw')

    @property
    def headers(self):
        headers = {
            'Authorization': f"Bearer {self.api_key}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            "Oasis-Appid": "10200",
            "Oasis-Webid": "084fa0d9cc98dc6b005db9b6e9d24056d0af3532",
            "Oasis-Platform": "web",
            "Oasis-Token": self.api_key,
            "Oasis-DeviceID": "084fa0d9cc98dc6b005db9b6e9d24056d0af3532",


        }
        return headers


if __name__ == '__main__':
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY3RpdmF0ZWQiOnRydWUsImFnZSI6NSwiYmFuZWQiOmZhbHNlLCJleHAiOjE3MTE0MzM1NDAsIm1vZGUiOjIsIm9hc2lzX2lkIjo4MzU0NzEyNzUwMjAxMjQxNiwidmVyc2lvbiI6MX0.HUSmIMGZaQQ7H_wRqiqeFul2rgUrZVtytrKCOanDFKE...eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOjEwMjAwLCJkZXZpY2VfaWQiOiIwODRmYTBkOWNjOThkYzZiMDA1ZGI5YjZlOWQyNDA1NmQwYWYzNTMyIiwiZXhwIjoxNzEyNzE5NDk3LCJvYXNpc19pZCI6ODM1NDcxMjc1MDIwMTI0MTYsInZlcnNpb24iOjF9.fupY0-Uks4wjFBj3BNtFNff4NUPDKDk7dVWxcRUVBoA"
    access_token = Completions(api_key=token).get_access_token()

    headers = {
        'Authorization': f"Bearer {access_token}",
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',

        "Content-Type": "application/connect+json",

        # "Content-Type": "application/json"

        "Oasis-Appid": "10200",
        "Oasis-Webid": "084fa0d9cc98dc6b005db9b6e9d24056d0af3532",
        "Oasis-Platform": "web",

        "Oasis-Token": access_token,
        "Oasis-DeviceID": "084fa0d9cc98dc6b005db9b6e9d24056d0af3532",

    }
    url = "https://stepchat.cn/api/proto.chat.v1.ChatMessageService/SendMessageStream"
    #
    payload = {"chatId":"83776330600574976","messageInfo":{"text":"11"}}
    #
    response = httpx.post(url, json=payload, headers=headers)



