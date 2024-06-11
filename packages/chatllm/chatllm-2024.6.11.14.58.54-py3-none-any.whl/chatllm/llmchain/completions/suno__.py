#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : suno
# @Time         : 2024/3/27 20:37
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import httpx

from meutils.pipe import *

url = "https://clerk.suno.ai/v1/client?_clerk_js_version=4.70.5"

api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImNsaWVudF8yZUluMHBQZEFFWlpoNjVtY0hvNFpncG95SkoiLCJyb3RhdGluZ190b2tlbiI6IjR5Z2R4dHR2ODY4OWh6dm56cWM4cWhkdnVpeDY1a21mMzZ0ajJtc2MifQ.lmzIvyYCCMQ_vNdGJO_WKPG2ptjK3gj16is5PUy0TRdQKjTj05BJCfXg5IMCWURghIFC5C4mKdzfKrz7ld0AMclvecc87NeKVtPB4WIHaoV9PN_eIkCT6heJHgd6fp_dhrlqNAI6NJtIewbfko4Q9RcYsJYyfesiKY5FhzEvphfzX3Og35luV8COSNfRfbu3Kv6zpifNIDAhGPHtjT4vQo6TucCsO4vjbNl0PYgJHYMDtmUxaq8bppxj2lcORen94w5oy33zqHE1O0UGFnE248sYib-LLeuoTWnH0uvDe03ovGRJ1H0Tk1e8fiKC4Y0q90zAe46FiyEV0I9V_yUdUA"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Cookie": f"__client={api_key}"
}

response = httpx.get(url, headers=headers).json()

sid = response.get("response", {}).get("last_active_session_id")
# access_token = response.get("response", {}).get("sessions", [{}])[0].get("last_active_token", {}).get("jwt")
# headers.update({"Authorization": f"Bearer {access_token}"})

url = f"https://clerk.suno.ai/v1/client/sessions/{sid}/tokens?_clerk_js_version=4.70.5"
response = httpx.post(url, headers=headers).json()  # refresh
access_token = response.get('jwt')
headers.update({"Authorization": f"Bearer {access_token}"})
#
# url = "https://studio-api.suno.ai/api/generate/v2"
# payload = {
#     "gpt_description_prompt": prompt,
#     "mv": "chirp-v3-0",
#     "prompt": "",
#     "make_instrumental": False,
# }
# if is_custom:
#     payload["prompt"] = prompt
#     payload["gpt_description_prompt"] = ""
#     payload["title"] = title
#     if not tags:
#         payload["tags"] = random.choice(MUSIC_GENRE_LIST)
#     else:
#         payload["tags"] = tags
#     print(payload)


# 歌词生成
# "https://studio-api.suno.ai/api/generate/lyrics/"
# POST {"prompt":""}
# {"id": "e719c37e-d724-401a-8519-d30c5f538f72"}
# GET https://studio-api.suno.ai/api/generate/lyrics/e719c37e-d724-401a-8519-d30c5f538f72
# {
#     "text": "[Verse]\nWalking down the boulevard, city lights shining bright\nFeeling the rhythm of the night as we dance the night away\nWe're strangers in this town, but our hearts beat as one\nLost in the moment, caught up in this neon love affair (ooh-yeah)\n\n[Verse 2]\nWe chase the stars in the sky, letting go of all our fears\nWe're living for the thrill, living for the here and now\nGuided by the music, we surrender to the beat\nIn this electric paradise, we find our escape (ooh-yeah)\n\n[Chorus]\nWe're caught up in this neon love affair (ooh-ooh)\nThe city's on fire, we're burning with desire (ooh-ooh)\nWith every heartbeat, we ignite the night (ignite the night)\nIn this neon love affair, we come alive (come alive)",
#     "title": "Neon Love Affair",
#     "status": "complete"
# }
class SunoRequest(BaseModel):
    """
    Welcome to Custom Mode 欢迎使用自定义模式

    Start with Lyrics: Write down your thoughts, or hit “Make Random Lyrics” for spontaneous creativity. Prefer no words? Opt for “Instrumental” and let the tunes express themselves.
    从歌词开始写下你的想法，或点击 "制作随机歌词 "进行即兴创作。不喜欢歌词？选择 "乐器"，让曲调来表达自己。

    Choose a Style: Select your “Style of Music” to set the vibe, mood, tempo and voice. Not sure? “Use Random Style” might surprise you with the perfect genre.
    选择风格：选择您的 "音乐风格"，设定氛围、情绪、节奏和声音。不确定？"使用随机风格 "可能会让你惊喜地发现完美的音乐风格。

    Extend Your Song: Want to go longer? Use the more actions (…) menu, select "Continue From This Song", select the desired time to extend your song from, and press Create. Use “Get Full Song” to put the full song together.
    延长您的歌曲：想延长时间？使用 "更多操作"（...）菜单，选择 "从这首歌开始继续"，选择想要延长歌曲的时间，然后按 "创建"。使用 "获取完整歌曲 "将完整歌曲放在一起。

    Unleash Your Creativity: Dive into the world of music-making and let your imagination run wild. Happy composing! 🎉
    释放你的创造力：潜入音乐创作世界，尽情发挥你的想象力。祝您创作愉快🎉
    """

    song_description: str  # '一首关于在雨天寻找爱情的富有感染力的朋克歌曲' todo: gpt润色
    """
        Describe the style of music and topic youwant (e.g. acoustic pop about theholidays).
        Use genres and vibes insteadof specific artists and songs
    """

    instrumental: bool = False
    """创作一首没有歌词的歌曲。"""

    custom_mode: bool = ''
    """Suno 专为创作原创音乐而设计。请确认您只提交人工智能生成的歌词、原创歌词或您有权继续使用的歌词。"""

    title: str = 'Neon Love Affair'

    music_style: str = 'pop'  # 可随机
    tags: str = music_style

    mv: str = 'chirp-v3-0'

    lyrics: Optional[str] = None  # 自动生成
    prompt: Optional[str] = None  # 自动生成
    """
        [Verse]
        Wake up in the morning, feeling kind of tired
        Rub my eyes, stretch my limbs, try to get inspired
        Open up the cupboard, see that shiny little jar
        It's my secret weapon, helps me reach the stars

        [Verse 2]
        Fill my favorite mug with that dark and steamy brew
        Inhale the aroma, it's my daily rendezvous
        Sip it nice and slow, feel the warmth flow through my veins
        Oh, coffee in the morning, you're my sugar, you're my dreams

        [Chorus]
        Coffee in the morning, you're my lifeline, can't deny
        You bring me energy when the day is looking gray
        Coffee in the morning, you're my sunshine in a cup
        With every sip, I'm feeling alive, ready to seize the day
    """
    # 继续创作
    continue_at: Optional[float] = None
    continue_clip_id: Optional[str] = None  # "8c7f666a-4df6-4657-8a83-d630b2b8ab56"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt = self.song_description
        self.tags = self.music_style
