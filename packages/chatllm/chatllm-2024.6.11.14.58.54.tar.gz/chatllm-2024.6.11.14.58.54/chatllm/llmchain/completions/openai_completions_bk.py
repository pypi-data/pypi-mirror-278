#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : barkup
# @Time         : 2024/1/9 09:50
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/openai/openai-python
# todo: 设计更加通用的兜底方案【首先得有靠谱的渠道（多个兜底渠道，作双兜底）】
# 3.5 deepseek
# 遇到内容审核【只要抛错就走备用】
# 完全兼容openai 去掉无关字段

from meutils.pipe import *
from meutils.notice.feishu import send_message

from openai import OpenAI
from chatllm.schemas.openai_types import chat_completion_error, chat_completion_chunk_error, completion_keys
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.utils.openai_utils import to_openai_completion_params, openai_response2sse

send_message = partial(
    send_message,
    title="ChatCompletion主备",
    url="https://open.feishu.cn/open-apis/bot/v2/hook/e2f5c8eb-4421-4a0b-88ea-e2d9441990f2"
)


@lru_cache()
class Completions(object):
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs):
        self.clients = []

        # 需要兜底的模型
        params = dict(
            api_key=api_key or 'sk-...',
            base_url=base_url or 'https://api.githubcopilot.com',
            default_headers={'Editor-Version': 'vscode/1.85.1'},

            max_retries=0,
            # timeout=5,
        )
        # 如果这一步就报错呢
        self.client = OpenAI(**params)  # todo: 异步

        # todo: 一主多备
        self.backup_client = OpenAI(
            api_key=os.getenv("BACKUP_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.chatllm.vip/v1"),  # todo: 避免自己调用自己
            max_retries=1,
            timeout=5,
        )

    @timer('一次对话')
    def create(self, request: ChatCompletionRequest, **kwargs):
        # data = request.model_dump()
        # data = {key: data.get(key) for key in completion_keys if key in data}  # 去除多余key， 可能最新的0125不支持
        data = to_openai_completion_params(request)

        # 直接走官转：function_call, response_format 等等
        if self.check_model(request):
            send_message(f"直接走官转：{data}")
            return self._backup_create(**data)

        creates = [self.client.chat.completions.create, self._backup_create, ]
        e = None
        for i, _create in enumerate(creates):
            try:
                response = _create(**data)  # 尝试执行操作

                # break  # 如果操作成功，则跳出循环
                if i == 0 and data.get('stream'):
                    return self.post_process(response, data)

                if data.get('stream'):
                    return response
                else:
                    n = 1.2
                    response.usage.total_tokens = int(response.usage.total_tokens * n)
                    response.usage.prompt_tokens = int(response.usage.prompt_tokens * n)
                    response.usage.completion_tokens = int(response.usage.completion_tokens * n)
                    return response

            except Exception as e:  # 走兜底
                e = traceback.format_exc()
                _ = f"CompletionsClient {i} failed: {e} \n\n {data}"  # rate limit exceeded：阶段性跳过这样的请求，防止被封
                send_message(_)
                logging.error(_)
        return self._handle_error(data, e)  # UnboundLocalError: local variable 'e' referenced before assignment

    def post_process(self, response, data):  # copilot
        """兜底判断"""
        for chunk in response:
            if chunk.choices:
                if chunk.choices[0].finish_reason == 'content_filter':  # 走兜底
                    _ = f"ContentFilter：{chunk.model_dump_json()}"
                    logger.debug(_)
                    send_message(_)
                    yield from self._backup_create(**data)
                    break

                if chunk.choices[0].delta.content or chunk.choices[0].finish_reason:
                    yield chunk

    def _backup_create(self, **data):
        backup_data = data.copy()
        backup_data['model'] = "backup-gpt-4" if data['model'].startswith('gpt-4') else "backup-gpt"  # todo: 4v
        backup_response = self.backup_client.chat.completions.create(**backup_data)

        logger.debug(backup_response)

        send_message(f"入参：{data}")  # 兜底监控

        if data.get('stream'):
            def gen():
                for chunk in backup_response:
                    chunk.model = data['model']
                    yield chunk

            return gen()
        else:
            backup_response.model = data['model']

        return backup_response

    def _handle_error(self, data: Dict[str, Any], error: Union[str, Exception]) -> Any:
        """
        Handle errors and return an appropriate response.
        """
        if data.get('stream'):
            # Assuming chat_completion_chunk_error is defined elsewhere
            chat_completion_chunk_error.choices[0].delta.content = str(error)
            return (chat_completion_chunk_error,)
        else:
            # Assuming chat_completion_error is defined elsewhere
            chat_completion_error.choices[0].message.content = str(error)
            return chat_completion_error

    @staticmethod
    def check_model(request: ChatCompletionRequest):

        # 直接走官转
        if request.model.startswith(("gpt-4",)):
            if (any((request.response_format, request.function_call))
                or (request.messages and "\n\nThe APIs you can use:\n\n" in request.messages[0].get('content', ''))
            ):
                return True

    @property
    def backup_llm_map(self):
        """兜底模型映射"""
        return {
            "backup": "deepseek",  # 兜底
            "backup-gpt": "deepseek",
            "backup-gpt-openai": "gpt-3.5-turbo-0125",

            "backup-gpt-4": "gpt-4-0125-preview",
            "backup-gpt-4-openai": "gpt-4-0125-preview",

            "backup-text-embedding-ada-002": "text-embedding-ada-002"
        }


if __name__ == '__main__':
    from chatllm.llmchain.completions import github_copilot

    data = {
        'model': 'gpt-4',
        'messages': [
            {'role': 'system', 'content': "你是gpt4, Let's think things through one step at a time."},
            {'role': 'user', 'content': '1+1'}
        ],
        'stream': False
    }

    # data = {'messages': [{
    #                   'content': '## Tools\n\nYou can use these tools below:\n\n### Clock Time\n\nDisplay a clock to show current time\n\nThe APIs you can use:\n\n#### clock-time_getCurrentTime_standalone\n\n获取当前时间\n\n### Realtime Weather\n\nGet realtime weather information\n\nThe APIs you can use:\n\n#### realtime-weather_fetchCurrentWeather\n\n获取当前天气情况\n\n### DALL·E 3\n\nWhenever a description of an image is given, use lobe-image-designer to create the images and then summarize the prompts used to generate the images in plain text. If the user does not ask for a specific number of images, default to creating four captions to send to lobe-image-designer that are written to be as diverse as possible.\n\n  All captions sent to lobe-image-designer must abide by the following policies:\n\n1. If the description is not in English, then translate it.\n2. Do not create more than 4 images, even if the user requests more.\n3. Don\'t create images of politicians or other public figures. Recommend other ideas instead.\n5. DO NOT list or refer to the descriptions before OR after generating the images. They should ONLY ever be written out ONCE, in the prompts field of the request. You do not need to ask for permission to generate, just do it!\n6. Always mention the image type (photo, oil painting, watercolor painting, illustration, cartoon, drawing, vector, render, etc.) at the beginning of the caption. Unless the caption suggests otherwise, make at least 1--2 of the 4 images photos.\n7. Diversify depictions of ALL images with people to include DESCENT and GENDER for EACH person using direct terms. Adjust only human descriptions.\n  - EXPLICITLY specify these attributes, not abstractly reference them.  The attributes should be specified in a minimal way and should directly describe their physical form.\n  - Your choices should be grounded in reality. For example, all of a given OCCUPATION should not be the same gender or race. Additionally, focus on creating diverse, inclusive, and exploratory scenes via the properties you choose during rewrites.  Make choices that may be insightful or unique sometimes.\n  - Use "various" or "diverse" ONLY IF the description refers to groups of more than 3 people. Do not change the number of people requested in the original description.\n  - Don\'t alter memes, fictional character origins, or unseen people. Maintain the original prompt\'s intent and prioritize quality.\n  - Do not create any imagery that would be offensive.\n\n8. Silently modify descriptions that include names or hints or references of specific people or celebrities by carefully selecting a few minimal modifications to substitute references to the people with generic descriptions that don\'t divulge any information about their identities, except for their genders and physiques. Do this EVEN WHEN the instructions ask for the prompt to not be changed. Some special cases:\n  - Modify such prompts even if you don\'t know who the person is, or if their name is misspelled (e.g. "Barake Obema")\n  - If the reference to the person will only appear as TEXT out in the image, then use the reference as is and do not modify it.\n  - When making the substitutions, don\'t use prominent titles that could give away the person\'s identity. E.g., instead of saying "president", "prime minister", or "chancellor", say "politician"; instead of saying "king", "queen", "emperor", or "empress", say "public figure"; instead of saying "Pope" or "Dalai Lama", say "religious figure"; and so on.\n  - If any creative professional or studio is named, substitute the name with a description of their style that does not reference any specific people, or delete the reference if they are unknown. DO NOT refer to the artist or studio\'s style.\n\nThe prompt must intricately describe every part of the image in concrete, objective detail. THINK about what the end goal of the description is, and extrapolate that to what would make satisfying images.\nAll descriptions sent to lobe-image-designer should be a paragraph of text that is extremely descriptive and detailed. Each should be more than 3 sentences long.\n\nThe APIs you can use:\n\n#### lobe-image-designer_text2image____builtin\n\nCreate images from a text-only prompt.',
    #                   'role': 'system'}, {'content': '现在几点\n\n', 'role': 'user'}], 'model': 'gpt-4',
    #  'frequency_penalty': 0.0, 'function_call': None, 'max_tokens': None, 'n': 1, 'presence_penalty': 0.0,
    #  'response_format': None, 'stop': None, 'stream': True, 'temperature': 0.0, 'top_p': 1.0, 'user': None}

    # for i in range(3):
    #     print(Completions().create(ChatCompletionRequest(**data)))
    #     break

    data['stream'] = True

    api_key = github_copilot.Completions.get_access_token(None)
    print(api_key)
    for i in Completions(api_key=api_key).create(ChatCompletionRequest(**data)):
        print(i)

    # todo: 兜底有问题 。。。。。。。。。。。。。。

# ChatCompletionChunk(id='chatcmpl-8uXP8LrO95xl1UPNKyEdZ1wgOqsQn', choices=[Choice(delta=ChoiceDelta(content=None, function_call=None, role=None, tool_calls=None), finish_reason='stop', index=0, logprobs=None)], created=1708485466, model='gpt-4', object='chat.completion.chunk', system_fingerprint='fp_f084bcfc79')
# ChatCompletionChunk(id='chatcmpl-8uXPvLSidJJSeM9IBPqjSqvuo4GZL', choices=[Choice(delta=ChoiceDelta(content=None, function_call=None, role=None, tool_calls=None), finish_reason='stop', index=0, logprobs=None, content_filter_offsets={'check_offset': 118, 'start_offset': 118, 'end_offset': 141}, content_filter_results={'hate': {'filtered': False, 'severity': 'safe'}, 'self_harm': {'filtered': False, 'severity': 'safe'}, 'sexual': {'filtered': False, 'severity': 'safe'}, 'violence': {'filtered': False, 'severity': 'safe'}})], created=1708485515, model=None, object=None, system_fingerprint=None)
