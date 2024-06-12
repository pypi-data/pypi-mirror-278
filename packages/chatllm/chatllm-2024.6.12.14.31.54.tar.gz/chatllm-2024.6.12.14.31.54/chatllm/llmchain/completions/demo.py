#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : demo
# @Time         : 2024/3/27 22:51
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import json

from meutils.pipe import *


# [**任务执行**](………………………………………….)✅
# 直接转df2md、优化超链接、
class A(BaseModel):
    id: str
    video_url: str = ''
    audio_url: str = ''
    image_url: str = 'https://cdn1.suno.ai/image_3d142559-b637-4f3a-8095-dcaaa512cc8c.png'
    image_large_url: str = 'https://cdn1.suno.ai/image_large_3d142559-b637-4f3a-8095-dcaaa512cc8c.png'
    major_model_version: str = 'v3'
    model_name: str = 'chirp-v3'
    metadata: dict = {}  # 元数据信息
    is_liked: bool = True
    user_id: str = '6275effb-094c-439a-8218-914fb33444ff'
    is_trashed: bool = True
    reaction: Optional[str] = None
    created_at: str = '2024-03-27T14:30:44.463Z'
    status: str = 'queued'
    title: str = 'Electric Dreams'
    play_count: int = 0
    upvote_count: int = 0
    is_public: bool = True


s = """
    {
        "id": "3d142559-b637-4f3a-8095-dcaaa512cc8c",
        "video_url": "",
        "audio_url": "",
        "image_url": "https://cdn1.suno.ai/image_3d142559-b637-4f3a-8095-dcaaa512cc8c.png",
        "image_large_url": "https://cdn1.suno.ai/image_large_3d142559-b637-4f3a-8095-dcaaa512cc8c.png",
        "major_model_version": "v3",
        "model_name": "chirp-v3",
        "metadata": {
            "tags": "futuristic electropop",
            "prompt": "[Verse]\nI'm standing on a rooftop, looking at the stars tonight\nMy heart is racing, can't wait for the morning light (ooh-yeah)\nI've got a feeling, something's gonna change my life\nI'm ready for the ride, can you feel it too?\n\n[Verse 2]\nThe city's buzzing, there's magic in the air\nIn every heartbeat, a dream is born and shared (ooh-yeah)\nWe're chasing rainbows, reaching for the stars above\nWe're gonna make it happen, together we'll fly high\n\n[Chorus]\nElectric dreams, they ignite the fire inside of me (oh-oh-oh)\nWith every beat, my heart skips and my spirit's free (my spirit's free)\nIn these electric dreams, we'll soar above the clouds (above the clouds)\nUnlock the possibilities, shout it out loud (shout it out loud)",
            "gpt_description_prompt": null,
            "audio_prompt_id": "8c7f666a-4df6-4657-8a83-d630b2b8ab56",
            "history": [
                {
                    "id": "8c7f666a-4df6-4657-8a83-d630b2b8ab56",
                    "continue_at": 68.04
                }
            ],
            "concat_history": null,
            "type": "gen",
            "duration": 68.04,
            "refund_credits": false,
            "stream": true,
            "error_type": null,
            "error_message": null
        },
        "is_liked": false,
        "user_id": "6275effb-094c-439a-8218-914fb33444ff",
        "is_trashed": false,
        "reaction": null,
        "created_at": "2024-03-27T14:30:44.463Z",
        "status": "queued",
        "title": "Electric Dreams",
        "play_count": 0,
        "upvote_count": null,
        "is_public": false
    }

""".strip()

print(json.loads(s))


def func(s):
    if s.endswith(".mp3"):
        return f"[🎧点击听歌]({s})"

    elif s.endswith(".mp4"):
        return f"[🖥点击观看]({s})"

    elif s.endswith(".png"):
        return f"![🖼]({s})"

    else:
        return f"```{s}```"


