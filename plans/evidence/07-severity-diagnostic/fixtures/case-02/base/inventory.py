def summary(items):
    return f"Items: {len(items)}."


def data(items):
    return {"count": len(items), "items": list(items)}
