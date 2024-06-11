#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_types
# @Time         : 2023/12/19 09:46
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai._types import FileTypes

completion_keys = get_function_params()


class SpeechCreateRequest(BaseModel):
    input: str
    model: str = 'tts'
    voice: str = "alloy"
    response_format: Literal["mp3", "opus", "aac", "flac", "wav", "pcm"] = "mp3"
    speed: float = 1


# class ASRRequest(BaseModel):
#     file: FileTypes
#     model: str = "whisper-1"
#     language: Optional[str] = None
#     prompt: Optional[str] = None
#     response_format: Literal["json", "text", "srt", "verbose_json", "vtt"] = "json"
#     temperature: Optional[str] = None
#     timestamp_granularities: List[Literal["word", "segment"]] = None


# todo: 结构体
chat_completion = {
    "id": "chatcmpl-id",
    "object": "chat.completion",
    "created": 0,
    "model": "LLM",
    "choices": [
        {
            "message": {"role": "assistant", "content": ''},
            "index": 0,
            "finish_reason": "stop",
            "logprobs": None
        }
    ],
    "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0}

}

chat_completion_chunk = {
    "id": "chatcmpl-id",
    "object": "chat.completion.chunk",
    "created": 0,
    "model": "LLM",
    "choices": [
        {
            "delta": {"role": "assistant", "content": ''},
            "index": 0,
            "finish_reason": None,
            "logprobs": None
        }
    ]
}

chat_completion_chunk_stop_ = {
    "id": "chatcmpl-8pFbEr4Y0L6RjW5hIGgDwSbiD991v",
    "choices": [
        {"delta": {"content": "", "function_call": None, "role": None, "tool_calls": None},
         "finish_reason": "stop",
         "index": 0,
         "logprobs": None
         }
    ],
    "created": 1707225384,
    "model": "gpt-4-turbo",

    "object": "chat.completion.chunk",
    "system_fingerprint": "fp_04f9a1eebf"
}

# 通用
chat_completion = ChatCompletion.model_validate(chat_completion)
chat_completion_chunk = ChatCompletionChunk.model_validate(chat_completion_chunk)
chat_completion_chunk_stop = ChatCompletionChunk.model_validate(chat_completion_chunk_stop_)

# ONEAPI_SLOGAN
ONEAPI_SLOGAN = os.getenv("ONEAPI_SLOGAN", "\n\n[永远相信美好的事情即将发生.](https://api.chatllm.vip/)\n\n")

chat_completion_slogan = chat_completion.model_copy(deep=True)
chat_completion_slogan.choices[0].message.content = ONEAPI_SLOGAN

chat_completion_chunk_slogan = chat_completion_chunk.model_copy(deep=True)
chat_completion_chunk_slogan.choices[0].delta.content = ONEAPI_SLOGAN

# ERROR
chat_completion_error = chat_completion.model_copy(deep=True)
chat_completion_chunk_error = chat_completion_chunk.model_copy(deep=True)

# PPU
chat_completion_ppu = chat_completion.model_copy(deep=True)
chat_completion_ppu.choices[0].message.content = "按次收费"
chat_completion_ppu.choices[0].finish_reason = "stop"
chat_completion_chunk_ppu = chat_completion_chunk.model_copy(deep=True)
chat_completion_chunk_ppu.choices[0].delta.content = "按次收费"


class ImageRequest(BaseModel):
    prompt: str
    model: str = 'dall-e-3'
    n: int = 1
    quality: str = 'standard'
    response_format: Literal["url", "b64_json"] = "url"
    size: Literal["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"] = '1792x1024'  # 测试默认值
    style: Literal["vivid", "natural"] = "vivid"
    extra_body: dict = {}


# ChatCompletionUserMessageParam
class ChatCompletionContentTextPart(BaseModel):
    """A part of the content of a message."""
    text: str
    """The text of the content part."""
    type: Literal["text", "image", "video", "audio", "file"]
    """The type of the content part."""


class ChatCompletionContentImagePart(BaseModel):
    """A part of the content of a message."""
    text: str
    """The text of the content part."""
    type: Literal["text", "image", "video", "audio", "file"]
    """The type of the content part."""


class ChatCompletionUserMessage(BaseModel):
    role: str = "user"
    """The role of the messages author, in this case `user`."""

    # content: Union[str, List[ChatCompletionContentPart]]
    """The contents of the user message."""


class BatchRequest(BaseModel):
    completion_window: Literal["24h"]
    """The time frame within which the batch should be processed.

    Currently only `24h` is supported.
    """

    endpoint: str = "/v1/chat/completions"  # Literal["/v1/chat/completions", "/v1/embeddings", "/v1/completions"]
    """The endpoint to be used for all requests in the batch.

    Currently `/v1/chat/completions`, `/v1/embeddings`, and `/v1/completions` are
    supported. Note that `/v1/embeddings` batches are also restricted to a maximum
    of 50,000 embedding inputs across all requests in the batch.
    """

    input_file_id: str
    """The ID of an uploaded file that contains requests for the new batch.

    See [upload file](https://platform.openai.com/docs/api-reference/files/create)
    for how to upload a file.

    Your input file must be formatted as a
    [JSONL file](https://platform.openai.com/docs/api-reference/batch/requestInput),
    and must be uploaded with the purpose `batch`. The file can contain up to 50,000
    requests, and can be up to 100 MB in size.
    """

    metadata: Dict[str, str] = {}
    """Optional custom metadata for the batch."""


if __name__ == '__main__':
    # data = {"stream": True, "model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "你好"}]}
    # print(ChatCompletionRequest(request=data).request)
    # print(chat_completion_error)
    # print(chat_completion_slogan)

    # print(chat_completion_chunk_stop)
    # for i in chat_completion_error:
    #     print(i)

    pass
    print(BatchRequest(input_file_id="input_file_id",
                       endpoint="/v1/chat/completions",
                       completion_window="24h",  # 完成时间只支持 24 小时
                       metadata={
                           "description": "Sentiment classification"
                       }))
