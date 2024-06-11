#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : suno
# @Time         : 2024/3/28 12:41
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.smooth_queue import SmoothQueue

from meutils.notice.feishu import send_message

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from chatllm.llmchain.completions import openai_completions
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.schemas.suno_types import SunoRequest

from chatllm.utils.openai_utils import to_openai_completion_params, openai_response2sse


# url = f"https://studio-api.suno.ai/api/feed/?ids={id1}%2C{id2}"
# 异步信息

class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')
        self.access_token = self.get_access_token(api_key=self.api_key)
        # self.client = httpx.Client(headers=self.headers, base_url="https://studio-api.suno.ai", follow_redirects=True)
        self.base_url = "https://studio-api.suno.ai"
        self.client = httpx.Client(base_url=self.base_url, follow_redirects=True)

    async def acreate(self, request: ChatCompletionRequest, **kwargs):
        request.model = request.model.startswith('gpt-4') and 'gpt-4' or 'gpt-3.5-turbo'
        data = to_openai_completion_params(request)

        start_time = time.perf_counter()

        try:
            _ = await self.client.chat.completions.create(**data)
        except Exception as e:
            logger.error(e)
            send_message(f"{self.api_key}\n{e}\n耗时：{time.perf_counter() - start_time} s",
                         "Copilot_token异常或者请求异常")

            # 备用
            data['model'] = 'backup-gpt'
            _ = await AsyncOpenAI().chat.completions.create(**data)

        # todo: 平滑操作
        if request.stream and data['model'].startswith('gpt-4'):
            return SmoothQueue().consumer(_, delay=0.055)

        return _

    def create(self, request: ChatCompletionRequest, **kwargs):
        prompts = request.messages[-1].get("content", "随便写一首歌").strip().split(maxsplit=1)

        suno = SunoRequest(title=prompts[0], song_description=prompts[-1])

        logger.debug(suno)

        # "https://cdn1.suno.ai/{song_id}.mp3"
        # "https://cdn1.suno.ai/{song_id}.mp3"

        # httpx.post("https://studio-api.suno.ai/api/generate/v2", data=suno.dict(), headers=c.get_headers(), follow_redirects=True)

        response = self.client.post("/api/generate/v2/", json=suno.dict(), headers=self.get_headers())

        # self.client.get
        return response.json()

    @property
    def total_credits_left(self) -> int:
        total_credits_left = self.client.get('/api/billing/info', headers=self.get_headers()).json().get(
            "total_credits_left")
        return total_credits_left

    @staticmethod
    @retrying(max_retries=1)
    @ttl_cache(ttl=60)
    def get_access_token(api_key: Optional[str] = None, dynamic_param=None):
        api_key = api_key or "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNsaWVudF8yZUluMHBQZEFFWlpoNjVtY0hvNFpncG95SkoiLCJyb3RhdGluZ190b2tlbiI6IjR5Z2R4dHR2ODY4OWh6dm56cWM4cWhkdnVpeDY1a21mMzZ0ajJtc2MifQ.lmzIvyYCCMQ_vNdGJO_WKPG2ptjK3gj16is5PUy0TRdQKjTj05BJCfXg5IMCWURghIFC5C4mKdzfKrz7ld0AMclvecc87NeKVtPB4WIHaoV9PN_eIkCT6heJHgd6fp_dhrlqNAI6NJtIewbfko4Q9RcYsJYyfesiKY5FhzEvphfzX3Og35luV8COSNfRfbu3Kv6zpifNIDAhGPHtjT4vQo6TucCsO4vjbNl0PYgJHYMDtmUxaq8bppxj2lcORen94w5oy33zqHE1O0UGFnE248sYib-LLeuoTWnH0uvDe03ovGRJ1H0Tk1e8fiKC4Y0q90zAe46FiyEV0I9V_yUdUA"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Cookie": f"__client={api_key}"
        }

        with httpx.Client() as client:
            url = "https://clerk.suno.ai/v1/client?_clerk_js_version=4.70.5"
            response = client.get(url, headers=headers).json()
            sid = response.get("response", {}).get("last_active_session_id")

            url = f"https://clerk.suno.ai/v1/client/sessions/{sid}/tokens?_clerk_js_version=4.70.5"
            response = client.post(url, headers=headers)  # refresh

        resp = response.json()
        resp['api_key'] = api_key
        _ = resp.get('jwt')  # token

        # logger.debug(resp)

        if not _:
            send_message(str(resp), "suno_token 异常")

        return _

    def get_headers(self):
        access_token = self.get_access_token(api_key=self.api_key)

        COMMON_HEADERS = {
            'Content-Type': 'text/plain;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            "Referer": "https://app.suno.ai/",
            "Origin": "https://app.suno.ai",
        }

        headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            "Authorization": f"Bearer {access_token}"
        }
        return {**COMMON_HEADERS, **headers}


if __name__ == '__main__':
    with timer():
        c = Completions()
        print(c.total_credits_left)

    prompt = """
        如何鉴别渣女
        瑜伽裤 健身房
        酒店 拍照 躺在床
        头等舱 上三亚
        露光背 拍一下
        秀厨艺 下午茶
        小小绿茶 你别惊讶
        朋友圈高逼格 银行卡里没余额
        约个会 黑丝腿
        """
    request = ChatCompletionRequest(messages=[{'role': 'user', 'content': prompt}])

    r = c.create(request)
    # df = pd.DataFrame(s['clips'])
    # df[['video_url', 'audio_url', 'image_url', 'model_name', 'created_at', 'metadata']]
    # metadata: audio_url、video_url、duration
    # s  = {'id': 'fbd295bb-1efd-453b-9ed4-88e9eadf6940', 'clips': [
    #     {'id': 'd8d813df-db75-44d5-9640-5330ee1e25af', 'video_url': '', 'audio_url': '', 'image_url': None,
    #      'image_large_url': None, 'major_model_version': 'v3', 'model_name': 'chirp-v3',
    #      'metadata': {'tags': 'pop', 'prompt': '', 'gpt_description_prompt': None, 'audio_prompt_id': None,
    #                   'history': None, 'concat_history': None, 'type': 'gen', 'duration': None, 'refund_credits': None,
    #                   'stream': True, 'error_type': None, 'error_message': None}, 'is_liked': False,
    #      'user_id': '6275effb-094c-439a-8218-914fb33444ff', 'is_trashed': False, 'reaction': None,
    #      'created_at': '2024-03-28T12:50:09.193Z', 'status': 'submitted', 'title': '如何鉴别渣女', 'play_count': 0,
    #      'upvote_count': 0, 'is_public': False},
    #     {'id': '77de0e97-2fe6-40ca-8494-210cad1168d8', 'video_url': '', 'audio_url': '', 'image_url': None,
    #      'image_large_url': None, 'major_model_version': 'v3', 'model_name': 'chirp-v3',
    #      'metadata': {'tags': 'pop', 'prompt': '', 'gpt_description_prompt': None, 'audio_prompt_id': None,
    #                   'history': None, 'concat_history': None, 'type': 'gen', 'duration': None, 'refund_credits': None,
    #                   'stream': True, 'error_type': None, 'error_message': None}, 'is_liked': False,
    #      'user_id': '6275effb-094c-439a-8218-914fb33444ff', 'is_trashed': False, 'reaction': None,
    #      'created_at': '2024-03-28T12:50:09.193Z', 'status': 'submitted', 'title': '如何鉴别渣女', 'play_count': 0,
    #      'upvote_count': 0, 'is_public': False}],
    #  'metadata': {'tags': 'pop', 'prompt': '', 'gpt_description_prompt': None, 'audio_prompt_id': None, 'history': None,
    #               'concat_history': None, 'type': 'gen', 'duration': None, 'refund_credits': None, 'stream': True,
    #               'error_type': None, 'error_message': None}, 'major_model_version': 'v3', 'status': 'running',
    #  'created_at': '2024-03-28T12:50:09.170Z', 'batch_size': 2}
