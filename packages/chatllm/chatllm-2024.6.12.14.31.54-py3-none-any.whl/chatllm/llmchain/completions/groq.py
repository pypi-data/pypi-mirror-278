#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : groq
# @Time         : 2024/2/20 16:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import requests

from meutils.pipe import *

url = "https://api.groq.com/v1/request_manager/text_completion"
data = {
    "system_prompt": "Please try to provide useful, helpful and actionable answers.",
    "user_prompt": "1+1",
    "model_id": "mixtral-8x7b-32768",
    # "history": [{"user_prompt": "讲个故事", "assistant_response": "好的，我来讲一个关于"}],
    "seed": 10,
    "max_tokens": 32768,
    "temperature": 0.2,
    "top_k": 40, "top_p": 0.8,
    "max_input_tokens": 21845
}
access_token = """
eyJhbGciOiJSUzI1NiIsImtpZCI6IjU1YzE4OGE4MzU0NmZjMTg4ZTUxNTc2YmE3MjgzNmUwNjAwZThiNzMiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiI5NTIwNjQ0MjA1OTAtc2ZiOG81NGxlcWQwZGViczZyZmNycWJ1ZmU0M2U3c2suYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhenAiOiJhbm9ueW1vdXMtYXBpLXVzZXJAZ3JvcS1jbG91ZC1zdGFnaW5nLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwiZW1haWwiOiJhbm9ueW1vdXMtYXBpLXVzZXJAZ3JvcS1jbG91ZC1zdGFnaW5nLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImV4cCI6MTcwODQyMDA0MSwiaWF0IjoxNzA4NDE2NDQxLCJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJzdWIiOiIxMTY4MjY2OTYyNzQ1NzAzNTg4NTcifQ.flEPxLXy4mYnrJwHofP-cd8I9HlXU1NOfHdgaQUPRj-2AEFsNFqouZB3HsrpqijoC1xeGpf7yKDfc1ryHvANHCDN1lzptkrI_rG3gg17Y_naqP-OKiUddYXXQEXAvSIOBlWRxO_NFjrhrbZCI9nXpUpcXfHSlOIluYZaqYbrJEAtgeeWjpFKRCWW1SVeorTWBrgO27_hOOy2AbvbLd7VKWPgjdii28jaF7t_O2PqHINzD7DMSXeDhbXaouKwhi7QqBChbmS8Q-K05VwEg6T9rQyaUVLH1RleW2n2tzRynjTOA91uj_XAo0Ol0o7GHyUWhNHFC-Fr92fjuGyBL83RCQ
""".strip()

headers = {
    'Authorization': f"Bearer {access_token}",  # access_token
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/119.0.0.0 Safari/537.36'
}

chunks = requests.post(url, json=data)
print(chunks.text)
#
# for i in chunks.iter_lines():
#     print(i)
