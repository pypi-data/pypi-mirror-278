#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : suno_api
# @Time         : 2024/4/3 16:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://suno.gcui.art/docs


from meutils.pipe import *

base_url = os.getenv("SUNO_BASE_URL")


def custom_generate_audio(payload):
    """
    {
      "prompt": "歌词",
      "tags": "pop metal male melancholic",
      "title": "歌名",
      "make_instrumental": False,
      "wait_audio": False,
    }

    :param payload:
    :return:
    """
    url = f"{base_url}/api/custom_generate"
    response = httpx.post(url, json=payload)
    return response.json()


def generate_audio_by_prompt(payload):
    """
    {
        "prompt": "A popular heavy metal song about war, sung by a deep-voiced male singer, slowly and melodiously. The lyrics depict the sorrow of people after the war.",
        "make_instrumental": False,
        "wait_audio": False
    }
    :param payload:
    :return:
    """
    url = f"{base_url}/api/generate"
    response = httpx.post(url, json=payload)
    return response.json()


def get_audio_information(audio_ids):
    url = f"{base_url}/api/get?ids={audio_ids}"
    response = httpx.get(url)
    return response.json()


def get_quota_information():
    url = f"{base_url}/api/get_limit"
    response = httpx.get(url)
    return response.json()


def song_info(df):
    """
    #   'audio_url': 'https://cdn1.suno.ai/63c85335-d8ec-4e17-882a-e51c2f358b2d.mp3',
    #   'video_url': 'https://cdn1.suno.ai/25c7e34b-6986-4f7c-a5f2-537dd80e370c.mp4',
    # https://cdn1.suno.ai/image_bea09d9e-be4a-4c27-a0bf-67c4a92d6e16.png
    :param df:
    :return:
    """
    df['🎵音乐链接'] = df['id'].map(
        lambda x: f"**请两分钟后试听**[🎧音频](https://cdn1.suno.ai/{x}.mp3)[▶️视频](https://cdn1.suno.ai/{x}.mp4)"
    )
    df['专辑图'] = df['id'].map(lambda x: f"![🖼](https://cdn1.suno.ai/image_{x}.png)")

    df_ = df[["id", "created_at", "model_name", "🎵音乐链接", "专辑图"]]

    return f"""
🎵 **「{df['title'][0]}」**

`风格: {df['tags'][0]}`

```toml
{df['prompt'][0]}
```


{df_.to_markdown(index=False).replace('|:-', '|-').replace('-:|', '-|')}
    """


from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.smooth_queue import SmoothQueue

from meutils.notice.feishu import send_message

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from chatllm.llmchain.completions import openai_completions
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo
from chatllm.schemas.suno_types import SongRequest
from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk as _chat_completion_chunk

from chatllm.utils.openai_utils import to_openai_completion_params, openai_response2sse

from langchain_community.chat_models import ChatOpenAI
from langchain.output_parsers import OutputFixingParser, PydanticOutputParser


class Completions(object):

    def __init__(self, api_key):
        self.httpx_aclient = httpx.AsyncClient(
            base_url=api_key,
            follow_redirects=True,
            timeout=30)

    async def acreate(self, request: ChatCompletionRequest):
        chat_completion_chunk = _chat_completion_chunk.model_copy(deep=True)

        async for content in self._acreate(request):
            chat_completion_chunk.choices[0].delta.content = content
            yield chat_completion_chunk

        # 结束标识
        chat_completion_chunk.choices[0].delta.content = ""
        chat_completion_chunk.choices[0].finish_reason = "stop"
        yield chat_completion_chunk

    @retrying
    async def _acreate(self, request: ChatCompletionRequest):
        """
        Song Description ： 200
        Lyrics：1250
        Style of Music：120
        Title：80
        """

        prompt = request.messages[-1]["content"]
        send_message(prompt)
        if prompt.startswith(("使用四到五个字直接返回这句话的简要主题",
                              "简要总结一下对话内容，用作后续的上下文提示 prompt，控制在 200 字以内")):
            return

        if "make_instrumental" in prompt:
            yield "> Auto Mode ✅：纯音乐模式\n\n"
            payload = {
                "gpt_description_prompt": prompt,
                "mv": 'chirp-v3-5',
                "prompt": "",
                "make_instrumental": True
            }
            df = await self.generate_by_prompt(payload)

        elif len(prompt.strip()) < 100:
            yield "> Auto Mode ✅: 生成歌词\n\n"
            payload = {
                "gpt_description_prompt": prompt,
                "mv": 'chirp-v3-5',
                "prompt": "",
                "make_instrumental": False
            }
            df = await self.generate_by_prompt(payload)

        else:

            song_request: SongRequest = self.prompt_parser(prompt)  # SongRequest
            payload = {
                "title": song_request.title,
                "tags": song_request.music_style,
                "prompt": song_request.lyrics,
                "continue_at": song_request.continue_at,
                "continue_clip_id": song_request.continue_clip_id,

                "mv": 'chirp-v3-5',

            }

            # title='My Song' lyrics='[Verse]...[Chorus]...[Bridge]...' music_style='Pop' continue_clip_id='8c7f666a-4df6-4657-8a83-d630b2b8ab56' continue_at=120
            # {
            #   "prompt": "string",
            #   "mv": "chirp-v3-0",
            #   "title": "string",
            #   "tags": "string",
            #   "continue_at": 120,
            #   "continue_clip_id": "string"
            # }
            send_message(str(payload))
            yield f"""```json\n{payload}\n```"""
            df = await self.custom_generate(payload)

        ids = ','.join(df['id'].tolist())  # df 为空

        yield f"""```\nTask ids: {ids}\n```\n\n"""
        yield f"""[音乐任务]("""

        for i in range(100):
            yield f"""{'🎵' if i % 2 else '🔥'}"""
            await asyncio.sleep(1)

            if i > 10:  # 5秒后才开始回调
                await asyncio.sleep(3)
                df = await self.get_information(ids)

                logger.debug("回调歌曲")

                if all(df.status == 'streaming'):  # 歌词生成
                    yield f""") ✅\n\n"""
                    _ = song_info(df)
                    yield _
                    send_message(_)
                    break
                elif all(df.status == 'error'):
                    yield f""") ❎\n\n"""
                    yield f"""⚠️触发内容审查，请修改后重试"""
                    send_message(df.to_markdown())
                    break

    def create_sse(self, request: ChatCompletionRequest):
        return openai_response2sse(self.acreate(request), redirect_model=request.model)

    @retrying
    async def custom_generate(self, payload):
        response = await self.httpx_aclient.post("/generate", json=payload)
        return pd.DataFrame(response.json().get('clips'))

    @retrying(min_seconds=3)
    async def generate_by_prompt(self, payload):
        response = await self.httpx_aclient.post("/generate/description-mode", json=payload)
        # print(response.json())
        return pd.DataFrame(response.json().get('clips'))

    @retrying
    async def get_information(self, ids):
        response0 = await self.httpx_aclient.get(f"/feed/{ids.split(',')[0]}")
        response1 = await self.httpx_aclient.get(f"/feed/{ids.split(',')[1]}")

        clips = response0.json() + response1.json()

        return pd.DataFrame([{**clip, **clip['metadata']} for clip in clips])

    def prompt_parser(self, prompt):
        song_parser = OutputFixingParser.from_llm(
            parser=PydanticOutputParser(pydantic_object=SongRequest),
            llm=ChatOpenAI(temperature=0),
            max_retries=2,
        )
        result = song_parser.parse(completion=prompt)  # 错误被自动修正
        return result


if __name__ == '__main__':
    prompt = """
    在10s处

    继续创作

    "6e579766-08ec-4b47-8674-1ebd6f3a366a"

    "make_instrumental\": true"

    """
    prompt += """
        请根据我的自定义歌词和音乐风格来创作歌曲：
        中文标题：酒入愁肠
        英文标题：Wine and Sorrows
        音乐风格：纯音乐

        歌词结构：
        [Intro]
        （独奏）

        [Verse 1]
        月光洒在破旧的篱笆，
        李白提壶独自彷徨。
        酒香飘逸入云端，
        笔下是豪迈的想象。

        [Chorus]
        一壶浊酒喜相逢，
        千载孤愁只杜甫懂。
        古道西风瘦马间，
        人间事，两行清泪长。

        [Verse 2]
        江水流淌带走忧伤，
        杜甫凝眉思国家。
        文章锋利剑如霜，
        心中苦，却言者无罪当。

        [Chorus]
        一壶浊酒喜相逢，
        千载孤愁只杜甫懂。
        古道西风瘦马间，
        人间事，两行清泪长。

        [Bridge]
        一千年来谁能懂，
        酒与愁是最深的重。
        历史长河波澜壮，
        诗人眼中看尽繁华空。

        [Chorus]
        一壶浊酒喜相逢，
        千载孤愁只杜甫懂。
        古道西风瘦马间，
        人间事，两行清泪长。

        [Outro]
        （独奏）

        音乐风格：
        传统民谣
        主要乐器：古筝、琵琶、笛子
        节奏：缓慢而深情
        氛围：沉郁、古典、充满历史感
    """
    print(Completions('http://154.3.0.117:39955').prompt_parser(prompt))

    # _ = arun(Completions('http://154.3.0.117:39955').generate_by_prompt({"gpt_description_prompt": "写首歌曲"}))
    # print(_)
    # payload = {
    #     "title": "Wine and Sorrows",
    #     "tags": "传统民谣",
    #     "prompt": "[Intro]\n（独奏）\n\n[Verse 1]\n月光洒在破旧的篱笆，\n李白提壶独自彷徨。\n酒香飘逸入云端，\n笔下是豪迈的想象。\n\n[Chorus]\n一壶浊酒喜相逢，\n千载孤愁只杜甫懂。\n古道西风瘦马间，\n人间事，两行清泪长。\n\n[Verse 2]\n江水流淌带走忧伤，\n杜甫凝眉思国家。\n文章锋利剑如霜，\n心中苦，却言者无罪当。\n\n[Chorus]\n一壶浊酒喜相逢，\n千载孤愁只杜甫懂。\n古道西风瘦马间，\n人间事，两行清泪长。\n\n[Bridge]\n一千年来谁能懂，\n酒与愁是最深的重。\n历史长河波澜壮，\n诗人眼中看尽繁华空。\n\n[Chorus]\n一壶浊酒喜相逢，\n千载孤愁只杜甫懂。\n古道西风瘦马间，\n人间事，两行清泪长。\n\n[Outro]\n（独奏）",
    #     "continue_at": 120,
    #     # "continue_clip_id": None,
    #     "mv": "chirp-v3-0"
    # }
    # _ = arun(Completions('http://154.3.0.117:39955').custom_generate(payload))
    # print(_)

#     data = generate_audio_by_prompt({
#         "prompt": "A popular heavy metal song about war, sung by a deep-voiced male singer, slowly and melodiously. The lyrics depict the sorrow of people after the war.",
#         "make_instrumental": False,
#         "wait_audio": False
#     })
#
#     # ids = f"{data[0]['id']},{data[1]['id']}"
#     # print(f"ids: {ids}")
#     #
#     # for _ in range(60):
#     #     data = get_audio_information(ids)
#     #     if data[0]["status"] == 'streaming':
#     #         print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
#     #         print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
#     #         break
#     #     # sleep 5s
#     #     time.sleep(5)
#
#     payload = {
#         "prompt": "我不是李白" * 100,
#         "tags": "pop metal male melancholic",
#         "title": "歌名",
#         # "make_instrumental": False,
#         # "wait_audio": False,
#     }
#
#     print(custom_generate_audio(payload))
# # {'error': 'Prompt, tags, and title are required'}
