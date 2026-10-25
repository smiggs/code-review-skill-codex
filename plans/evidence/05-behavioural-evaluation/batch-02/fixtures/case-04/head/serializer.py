import json


def status_payload():
    return json.dumps({"status": "ready"})
