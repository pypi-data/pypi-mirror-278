from typing import Any
from urllib.parse import urljoin
import json
from ..common.context import get_domain, get_by_headers

from ..credential import AppCredential
from ..common.util import get_http_session

defaultOptions = {
    "timeout": 60 * 1000 * 5,
    "retry_times": 0,
}


def call_action(
        action_api_name: str,
        action_data: dict,
        options=None,
        is_async=False,
) -> Any:
    if options is None:
        options = {}
    credential = AppCredential()
    token = credential.get_token()
    domain = get_domain()

    if not token:
        raise Exception('get token failed')

    http = get_http_session(token)
    current_skill_id = get_by_headers('x-aily-skill-instance-id')
    if current_skill_id is None and action_api_name == 'action:brn:cn:spring:all:all:connector_action_runtime' \
                                                       ':/spring_sdk_send_message':
        raise Exception('发送消息接口暂不支持直接调试，需要点击技能调试。')

    action_data.update({'skillInstanceID': current_skill_id})
    req = {
        'customerBizId': 'spring',
        'data': {
            'actionApiName': action_api_name,
            'actionData': json.dumps(action_data),
            'options': json.dumps({
                **defaultOptions,
                **options,
            }),
        },
        "isAsync": is_async
    }

    path = f'/ai/v1/connector_action/namespaces/{credential.namespace}/execute_action'  # noqa: E501
    url = urljoin(domain, path)
    res = http.post(url, json=req, timeout=options.get('timeout', defaultOptions.get('timeout')))

    if res.status_code != 200:
        raise Exception(f'call action failed: {res.text}')

    logid = res.headers.get('x-tt-logid')
    data = res.json()
    if data['code'] != '0':
        raise Exception(f'[{logid}] call action failed: {data}')

    if data['data']['code'] not in ['null', '200', '']:
        raise Exception(f'[{logid}] parse action response error: data is empty, {data}')

    if not data['data']['data']:
        raise Exception(f'[{logid}] parse action response error: data is empty, {data}')

    return json.loads(data['data']['data'])
