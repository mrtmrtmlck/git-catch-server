import base64
import json


def get_url(extension, params):
    base_url = 'http://localhost:3000/'

    if len(extension.value) > 0:
        base_url += extension.value

    if len(params) > 0:
        token = generate_token(params)
        base_url += f'?token={token}'

    return base_url


def generate_token(token_dict):
    return base64.urlsafe_b64encode(json.dumps(token_dict).encode('utf-8')).decode("utf-8")


def decode_token(token):
    return json.loads(base64.urlsafe_b64decode(token).decode('utf-8'))

