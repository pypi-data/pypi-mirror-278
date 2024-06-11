#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : gptall
# @Time         : 2024/3/13 14:06
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.notice.feishu import send_message
from meutils.str_utils.regular_expression import parse_url

from chatllm.schemas.openai_types import chat_completion, chat_completion_chunk
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest
from chatllm.utils.openai_utils import openai_response2sse, to_openai_completion_params

from openai import OpenAI, AsyncOpenAI


class Completions(object):

    def __init__(self, **client_params):
        self.api_key = client_params.get('api_key')
        self.client = AsyncOpenAI(
            api_key="sk-kVKomhMC01dfcz5N17A0E6D0FfB347CeB0323eEc143863Ae",
            base_url="https://api.zlrxjh.top/v1",
        )

        self.file_client = AsyncOpenAI(
            api_key=os.getenv('MOONSHOT_API_KEY'),
            base_url=os.getenv('MOONSHOT_BASE_URL'),
        )

    async def acreate(self, request: ChatCompletionRequest):
        """
        todo: 走低配版
        :param request:
        :return:
        """
        question = request.messages[-1]
        urls = parse_url(question.get('content', ''))
        for url in urls:
            async for chunk in self.file_extract(url):
                if isinstance(chunk, str):
                    request.messages.append({'role': 'user', 'content': chunk})  # pdf内容拼接在user里
                else:
                    yield chunk

        data = to_openai_completion_params(request, redirect_model='gpt-4-mobile')
        response = await self.client.chat.completions.create(**data)
        # async for chunk in response:
        #     yield chunk
        yield response

    def create_sse(self, request: ChatCompletionRequest):  # todo：非流式
        return openai_response2sse(self.acreate(request), redirect_model=request.model)

    async def file_extract(self, url: str):  # todo: 加缓存
        # urls = parse_url(content)

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url)
            if response.status_code != 200:
                chat_completion_chunk.choices[0].delta.content = f"\n> url error: {response.reason_phrase}\n"
                yield chat_completion_chunk
                return  # 应该是跳出

            file_object = await self.file_client.files.create(file=response.content, purpose="file-extract")

            # FileObject(id='cnoki7pkqq4r540f4q6g', bytes=154075, created_at=1710311711, filename='upload', object='file', purpose='file-extract', status='ok', status_details='')
            # status='error', status_details=''
            if file_object.status == 'ok':
                _ = file_object.model_dump_json()
                _ = f"\n```json\n{_}\n```\n"

                logger.debug(_)

                chat_completion_chunk.choices[0].delta.content = _
                yield chat_completion_chunk
            else:
                status_details = f"文件上传失败: {file_object.status_details}"
                send_message(status_details)
                chat_completion_chunk.choices[0].delta.content = f"\n```json\n{status_details}\n```\n"
                yield chat_completion_chunk
                return  # 应该是跳出

            # {
            #     "content": "2023年年度绩效面谈反馈表\n工号 7683 姓名 袁杰 岗位 金融算法工程师\n部门 信息科技部 中心 数据科学研发中心 上级 龚明升\n（1）做的好：\n 合规资讯全局和语义检索的实现，提高了搜索的准确性和效率。\n 智能文档解析服务项目的运行和文件服务器的建设，提高了文件处理的效率。\n 合规文档智能问答规丞相的实现，提供了一种基于大模型技术的新的用户交互方式。\n 爬虫需求的实现和优化，提高了数据获取的效率和准确性。\n 北斗客户旅程的客户分群模型的解释和优化，提高了模型的可解释性和准确性。\n（2）待优化：\n 合规宝典数据接入和更新的效率需要提高。\n 文档解析的准确率需要提高，目前的效果仍有待提升。\n 部分爬虫需求的实现存在问题，如部分网页附件下载失败，需要优化爬虫下载附件的逻辑。\n 部分合规资讯存在问题，如下载链接点击报错，文档中包含附件但无法下载等，需要进一步修复。\n 部分OCR解析需求的实现存在问题，需要进一步优化。\n 合规资讯bug的修复，提高了系统的稳定性。\n（3）24年重点工作：\n 继续优化合规宝典数据接入和更新的效率，目标是实现每日增量更新合规数据。\n 提高文档解析的准确率，包括常用类型的文档解析和特定类型（如财报）的文档解析。\n 优化爬虫需求的实现，解决部分网页附件下载失败等问题。\n 修复合规资讯存在的问题以及重构规丞相大模型智能问答，提高用户体验。\n 进一步优化OCR解析需求的实现，提高OCR识别的准确率。\n 进一步优化客户分群精准营销模型，提高模型的可解释性和准确性。\n 探索新的技术和方法，如Unstructured的可行性，大模型的升级和推理加速等。\n您在本周期的考评等级为 。\n员工对本次绩效考核结果的态度：\n 认同 □ 不认同 □ 无所谓\n员工签字\u0026日期：\n上级签字\u0026日期：\n\n说明：\n以上表格填写完成，由面谈双方签字后将原件或扫描件提交到部门负责人和 HRBP 处备案。",
            #     "file_type": "application/pdf", "filename": "upload", "title": "", "type": "file"
            # }

            yield await self.file_client.files.retrieve_content(file_id=file_object.id)
