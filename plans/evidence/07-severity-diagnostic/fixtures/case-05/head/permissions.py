RIGHTS = {"admin": {"read", "write"}, "reader": {"read"}}
ACTIONS = {"read", "write"}


def allowed(role, action):
    return action in ACTIONS and action in RIGHTS.get(role, set())
