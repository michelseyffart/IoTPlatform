import requests
import json
import logging
from openhab.config.paths import path_token
from openhab.config.config import *
import openhab.create_logger as logs

log = logs.get_logger(filename="http.log", name="http", consolelevel=logging.WARNING)

url = get_from_config("url_rest")

with open(path_token) as f:
    token = f.read()


def openhab_request(endpoint: str, method, payload: dict | str = None, content_type: str = 'application/json'):
    if payload and not isinstance(payload, str):
        payload = json.dumps(payload)
    _url = url + endpoint
    headers = {
        'Accept-Language': '<string>',
        'Content-Type': content_type,
        'Accept': '*/*',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request(method, _url, headers=headers, data=payload)
    if response.ok:
        log.info(f"Successful: {response.status_code}")
        return response.status_code
    else:
        log.warning(f"Error: {response.status_code}\n{response.text}")
        return response.status_code
