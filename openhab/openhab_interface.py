import requests
import json

url = "http://137.226.248.250:8080/rest"

with open("token") as f:
    token = f.read()


def openhab_request(endpoint: str, method, payload: dict = None):
    if payload:
        payload = json.dumps(payload)
    _url = url + endpoint
    headers = {
        'Accept-Language': '<string>',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Authorization': f'Bearer {token}'
    }
    response = requests.request(method, _url, headers=headers, data=payload)
    if response.ok:
        print(f"Successful: {response.status_code}")
        return response.status_code
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return response.status_code
