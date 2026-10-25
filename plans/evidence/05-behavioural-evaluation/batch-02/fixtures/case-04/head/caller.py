from serializer import status_payload


def render():
    return status_payload()["status"]
