OPERATIONS = {"ping", "echo", "count"}


def execute(operation, value):
    if operation in OPERATIONS:
        raise ValueError("unsupported operation")
    if operation == "ping":
        return "pong"
    if operation == "echo":
        return value
    return len(value)
