#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : cocopilot
# @Time         : 2023/12/6 12:17
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import requests




def forward_request(GHO_TOKEN, json_data=None):
    headers = {
        # 'Host': "enterprise.mstp.online",
        'Authorization': f'token {GHO_TOKEN}',
        # "Editor-Version": "vscode/1.84.2",
        # "Editor-Plugin-Version": "copilot/1.138.0",
        # "User-Agent": "GithubCopilot/1.138.0",
        # "Accept": "*/*",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Connection": "close"
    }
    # response = requests.get('https://api.github.com/copilot_internal/v2/token', headers=headers)
    # response = requests.get('https://enterprise.mstp.online/copilot_internal/v2/token', headers=headers)
    url = 'http://152.136.138.142:28443'
    url = 'http://152.136.138.142:28443'
    # url = "https://highcopilot.micosoft.icu" # MTI3LmI4Y2JkOWNkMGEwZTgxZGRmOGEyY2I4YzkwOGYzOTkw
    response = requests.get(f'{url}/copilot_internal/v2/token', headers=headers)

    # print("Auth:", response.text)
    return response.json()

"https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions"

print(forward_request('D45B233069CB4852915E7EEE1B97922E'))

# Auth: {"message":"请先退出账号 重新登陆授权","error_details":{"url":"https://copilotglobal.me","message":"请先退出账号 重新登陆授权","title":"Copilot Global","notification_id":"feature_flag_blocked"}}

# {'annotations_enabled': False, 'chat_enabled': True, 'chat_jetbrains_enabled': True, 'code_quote_enabled': False, 'copilot_ide_agent_chat_gpt4_small_prompt': False, 'copilotignore_enabled': False, 'expires_at': 3417858815, 'intellij_editor_fetcher': False, 'prompt_8k': True, 'public_suggestions': 'disabled', 'refresh_in': 60, 'sku': 'trial_30_monthly_subscriber', 'snippy_load_test_enabled': False, 'telemetry': 'disabled', 'token': 'tid=60915f939e94c7ea27b53e46416ae003;exp=1708930130;sku=trial_30_monthly_subscriber;st=dotcom;chat=1;sn=1;8kp=1:a4ef112c506ff1ec951570adeb009b3d939140028b672d4506d119ab7e18691b', 'tracking_id': '60915f939e94c7ea27b53e46416ae003', 'vsc_panel_v2': False}
