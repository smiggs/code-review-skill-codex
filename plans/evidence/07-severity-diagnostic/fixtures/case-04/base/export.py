def export_rows(values, page_size):
    remainder = len(values) % page_size
    full_end = len(values) - remainder
    result = []
    for start in range(0, full_end, page_size):
        result.extend(values[start:start + page_size])
    if remainder:
        result.extend(values[full_end:])
    return result
