def record_event(path, event):
    with path.open("w", encoding="utf-8") as stream:
        stream.write(event + "\n")
