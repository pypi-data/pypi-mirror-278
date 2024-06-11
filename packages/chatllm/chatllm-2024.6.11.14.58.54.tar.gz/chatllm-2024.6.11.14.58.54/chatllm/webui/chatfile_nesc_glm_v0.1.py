#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : st_chat
# @Time         : 2023/8/11 14:45
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import streamlit as st
# st.set_page_config('🔥ChatLLM', layout='wide', initial_sidebar_state='collapsed')

from openai import OpenAI
from meutils.serving.streamlit import hide_st_style, st_chat_message, ChatMessage

hide_st_style()


def gen(question):
    nesc = "\n`大模型根据公司相关法规及提问语义做答，不作为合规管理官方回复。`"

    data = {

        'model': '65f41c8a9c0ebbcbe28bb9c1',

        'messages': [
            {'role': 'user', 'content': question}
        ],
        'stream': True,

    }
    _ = OpenAI().chat.completions.create(**data)

    for chunk in _:
        if chunk.choices[0].finish_reason == 'stop':
            break
        yield chunk.choices[0].delta.content
    yield from nesc


if __name__ == '__main__':
    col1, col2, col3, *_ = st.columns(3)
    with col1:
        st.image('规丞相.png', width=64)
    with col2:
        st.markdown('##### ')
        st.markdown('##### ')
        st.markdown('##### 规丞相驾到')

    st.markdown('> ⚠️“规丞相”仅供东北证券内部测试使用，所做回答不得用于东北证券官方回复。')

    st_chat_message(ChatMessage(avatar="规丞相.png", generator="欢迎来找**规丞相**，您有什么要咨询的吗❓"))

    for message in st.session_state.messages:  # 设计his
        st_chat_message(message)

    print(st.session_state.messages)

    prompt = st.chat_input("    🤔 你可以问我任何问题", key='xx')  # 最下面
    if prompt:
        with st.spinner('AI 🤔'):
            st_chat_message(ChatMessage(name="user", generator=prompt), is_history=True)

            st_chat_message(ChatMessage(avatar="规丞相.png", generator=gen(prompt)), is_history=True)
