def get_record(records, record_id, tenant):
    record = records.get(record_id)
    if not tenant or record is None or record["tenant"] != tenant:
        return None
    return dict(record)
