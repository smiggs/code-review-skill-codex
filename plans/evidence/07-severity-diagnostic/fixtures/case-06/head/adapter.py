import json


def encode(pending):
    return json.dumps({"pending": pending})
