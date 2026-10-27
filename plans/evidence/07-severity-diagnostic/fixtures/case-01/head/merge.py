def incoming(records):
    merged = {}
    for supplier, invoice_id, amount in records:
        merged[invoice_id] = (supplier, invoice_id, amount)
    return list(merged.values())
