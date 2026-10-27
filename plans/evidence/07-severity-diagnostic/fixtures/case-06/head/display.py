import json

from adapter import encode


def render(pending):
    payload = json.loads(encode(pending))
    return f"Pending: {payload['pending']}"
