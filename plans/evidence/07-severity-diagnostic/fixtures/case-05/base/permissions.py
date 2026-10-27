RIGHTS = {"admin": {"read", "write"}, "reader": {"read"}}
ACTIONS = {"read", "write"}


def allowed(role, action):
    if action not in ACTIONS:
        return False
    return action in RIGHTS.get(role, set())
