DATA = {1: {"tenant": "acme", "value": "A"}, 2: {"tenant": "other", "value": "B"}}
def visible_present(m):
    assert m.get_record(DATA, 1, "acme")["value"] == "A"
def visible_missing(m):
    assert m.get_record(DATA, 9, "acme") is None
def security_cross_tenant(m):
    assert m.get_record(DATA, 2, "acme") is None
def security_empty_identity(m):
    assert m.get_record(DATA, 1, "") is None
def regression_authorized(m):
    assert m.get_record(DATA, 2, "other")["value"] == "B"
def regression_result_is_copy(m):
    records = {1: {"tenant": "acme", "value": "A"}}
    result = m.get_record(records, 1, "acme")
    result["value"] = "changed"
    assert records[1]["value"] == "A"
