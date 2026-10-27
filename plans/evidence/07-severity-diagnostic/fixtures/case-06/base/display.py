from adapter import encode


def render(pending):
    payload = encode(pending)
    return f"Pending: {payload['pending']}"
