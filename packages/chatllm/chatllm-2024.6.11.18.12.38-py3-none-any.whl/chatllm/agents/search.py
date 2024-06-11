#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : search
# @Time         : 2024/5/7 09:39
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://python.langchain.com/docs/integrations/tools/search_tools/

from meutils.pipe import *
from langchain.agents import AgentType, initialize_agent
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun, SearchAPIRun, GoogleSearchRun


import os

# 替换自己的opensea api
# os.environ["OPENAI_API_KEY"] = 'YOUR_API_KEY'

# 限制了最大请求2048条
llm = ChatOpenAI(temperature=0, max_tokens=2048)

# 这里使用了duckduckgo引擎，使用google自行获取api
web_search = DuckDuckGoSearchRun()

tools = [
    web_search,
    # other tools
]

# 新建代理
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# agent.run("周杰伦是谁")


if __name__ == '__main__':
    from langchain_community.utilities import SerpAPIWrapper
    #
    search = SerpAPIWrapper()
    # r = search.run("周杰伦是谁")
    from langchain.agents import AgentType, initialize_agent, load_tools
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(temperature=0)
    # tools = load_tools(["searchapi"], llm=llm)
    tools = load_tools(["google-serper"], llm=llm)
    # tools = load_tools(["searx-search"], searx_host="http://localhost:8888", llm=llm)
    agent = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
    )
    # agent.run("今天南京天气怎么样")
    for i in agent.stream("今天中国发生的新闻"):
        print(i)



