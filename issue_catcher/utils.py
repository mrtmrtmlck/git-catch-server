import base64
import json


def generate_token(token_dict):
    return base64.urlsafe_b64encode(json.dumps(token_dict).encode('utf-8')).decode("utf-8")


def decode_token(token):
    return json.loads(base64.urlsafe_b64decode(token).decode('utf-8'))

