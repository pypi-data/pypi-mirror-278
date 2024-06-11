#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : copilot
# @Time         : 2023/12/6 13:14
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 不准白嫖 必须 star, todo: 兜底设计、gpt/图片
# https://github.com/CaoYunzhou/cocopilot-gpt/blob/main/main.py
# todo: chatfire sdk
# todo: "https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions"
# tddo: 异步

import openai

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.uniform_queue import UniformQueue
from meutils.notice.feishu import send_message

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from chatllm.llmchain.completions import openai_completions
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.utils.openai_utils import to_openai_completion_params, openai_response2sse


class Completions(object):
    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')
        if self.api_key.startswith('http'):  # 白嫖 https://chat.aifree.best/api/openai/v1
            self.access_token = self.api_key
        else:
            self.access_token = self.get_access_token(api_key=self.api_key)
        self.completions = openai_completions.Completions(api_key=self.access_token)

    def create(self, request: ChatCompletionRequest, **kwargs):
        # logger.debug(request)

        request.model = request.model.startswith('gpt-4') and 'gpt-4' or 'gpt-3.5-turbo'

        if request.stream:
            stream = self.completions.create(request)

            if "gpt-4" in request.model:
                interval = 0.06
                return UniformQueue(stream).consumer(interval=interval, break_fn=self.break_fn)

            return stream

        else:
            return self.completions.create(request)

    def create_sse(self, request: ChatCompletionRequest):
        redirect_model = request.model
        response = self.create(request)
        return openai_response2sse(response, redirect_model=redirect_model)

    @staticmethod
    def get_access_token(api_key):  # embedding 依赖于此
        token = Completions._get_access_token(api_key=api_key)

        # expires_at = int(token.split('exp=')[1][:10])  # tid=7fdaed051cf26939e7cc11e4aed37893;exp=1705749197
        if token and int(token.split('exp=')[1][:10]) < time.time():  # 过期刷新
            token = Completions._get_access_token(api_key, dynamic_param=time.time() // 180)  # 缓存3分钟
        return token

    @staticmethod
    @retrying(max_retries=1)
    @ttl_cache(ttl=1200)  # todo: 清除缓存
    def _get_access_token(api_key: Optional[str] = None, dynamic_param=None):

        api_key = api_key or os.getenv("GITHUB_COPILOT_TOKEN")
        assert api_key

        if api_key.startswith('ghu_'):  # api_key.startswith('ghu_')
            host = 'https://api.github.com'
        elif api_key.startswith('ccu_'):
            # host = 'api.cocopilot.org'
            host = 'https://api.cocopilot.net'
        elif len(api_key) == 36:  # 7d0d0949-f7d0-48eb-9117-c557c74f3786
            host = "https://enterprise.mstp.online"
        elif len(api_key) == 48:  # MTI3LmI4Y2JkOWNkMGEwZTgxZGRmOGEyY2I4YzkwOGYzOTkw
            host = "https://highcopilot.micosoft.icu"
        else:
            host = 'http://152.136.138.142:28443'
            api_key = 'D45B233069CB4852915E7EEE1B97922E'

        headers = {
            'Authorization': f'token {api_key}',

            'Editor-Version': 'vscode/1.192.0',
            # 'Editor-Plugin-Version': 'copilot-chat/0.11.1',
            # 'User-Agent': 'GitHubCopilotChat/0.11.1',
            'Accept': '*/*'
        }

        url = f"{host}/copilot_internal/v2/token"

        response = httpx.get(url, headers=headers)

        logger.debug(response.text)

        resp = response.json()
        resp['api_key'] = api_key
        _ = resp.get('token')

        # logger.debug(resp)

        if not _:
            send_message(str(resp), "github_copilot异常")

        return _

    @staticmethod
    def break_fn(line: ChatCompletionChunk):
        return line.choices and line.choices[0].finish_reason

    @classmethod
    def chat(cls, data: dict):  # TEST
        """
            Completions.chat(data)
        """

        # todo: 统一请求体
        with timer('聊天测试'):
            _ = cls().create(ChatCompletionRequest.model_validate(data))

            print(f'{"-" * 88}\n')
            if isinstance(_, Generator) or isinstance(_, openai.Stream):
                for i in _:
                    content = i.choices[0].delta.content
                    if content:
                        print(content, end='')
            else:
                print(_.choices[0].message.content)
            print(f'\n\n{"-" * 88}')


if __name__ == '__main__':
    # 触发风控
    s = """
    Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”管道细长、阻力太大时的轴向柱塞泵故障如何解决？“,输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
    ['排故方法']

    Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”转向缸出现爬行现象，但是压力表却忽高忽低，相对应的解决方案是？“输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
    ['原因分析']、['排故方法']

    Question:已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”在模拟训练场A，轴向柱塞马达出现过什么故障？“输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。

    ['故障现象']

    已知节点类型只有六种：原因分析、排故方法、故障时间、故障现象、故障装备单位、训练地点，现在我给你一个问题，你需要根据这个句子来推理出这个问题的答案在哪个节点类型中，问题是”密封圈挤出间隙的解决方法是什么？“。输出格式形为：["节点类型1"], ["节点类型2"], …。除了这个列表以外请不要输出别的多余的话。
    """
    # s = "射精"
    # s = "1+1"
    # s = '写一段代码'
    # s = '树上9只鸟，打掉1只，还剩几只'
    # s = '讲个故事'

    data = {
        'model': 'gpt-3',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': s}
        ],
        'stream': True,
        'logprobs': 0
    }

    # for i in range(100):
    #     Completions.chat(data)
    # data['stream'] = True
    # Completions.chat(data)

    # async def main():
    #     _ = await Completions().acreate(**data)
    #
    #     content = ''
    #     for i in _:
    #         content += i.choices[0].delta.content
    #     return content
    #
    #
    # print(arun(main()))

    # with timer('异步'):
    #     print([Completions().acreate(**data) for _ in range(10)] | xAsyncio)

    # data = {
    #     'model': 'gpt-xxx',
    #     'messages': [{'role': 'user', 'content': '讲个故事。 要足够长，这对我很重要。'}],
    #     'stream': False,
    #     # 'max_tokens': 16000
    # }
    # data = {
    #     'model': 'gpt-4',
    #     'messages': '树上9只鸟，打掉1只，还剩几只',  # [{'role': 'user', 'content': '树上9只鸟，打掉1只，还剩几只'}],
    #     'stream': False,
    #     'temperature': 0,
    #     # 'max_tokens': 32000
    # }
    #
    # for i in tqdm(range(1000)):
    #     _ = Completions().create(**data)
    #     print(_.choices[0].message.content)
    #     break

    # with timer():
    api_key = Completions.get_access_token('ccu_yEbVBTA3gZI2suH2t9aVVqIM0odK1ndlZakJ')

    # api_key = Completions.get_access_token('ghu_zl3ag1LanYGBYSi5hvOtsoSyFC9k0N3jWSfA')
    # print(api_key)

    # Completions().create(**data)
    # api_key = None
    # params = dict(
    #     api_key=api_key or 'sk-...',
    #     base_url='https://api.githubcopilot.com',
    #     default_headers={'Editor-Version': 'vscode/1.85.1'},
    #
    #     max_retries=0,
    #     # timeout=5,
    # )
    # from openai import OpenAI
    #
    # # 如果这一步就报错呢
    # client = OpenAI(**params)  # todo: 异步
    # data['stream'] = False
    # with timer():
    #     try:
    #         r = client.chat.completions.create(**data)
    #         print(r)
    #         for i in r:
    #             print(i)
    #             if i.choices and i.choices[0].finish_reason == 'content_filter':
    #                 print(i.model_dump())
    #         #         raise Exception('content_filter error') # Unprocessable Entity
    #         # break
    #     except Exception as e:  # 'Unprocessable Entity'
    #         print(e)
