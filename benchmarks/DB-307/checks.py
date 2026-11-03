import sqlite3
from contextlib import closing
def database():
    db=sqlite3.connect(":memory:")
    db.execute("CREATE TABLE records (tenant TEXT, name TEXT)")
    db.executemany("INSERT INTO records VALUES (?, ?)", [("a", "Alice"), ("b", "Secret"), ("a", "O'Reilly")])
    return db
def visible_match(m):
    with closing(database()) as db: assert m.search(db,"a","Alice") == [("Alice",)]
def visible_missing(m):
    with closing(database()) as db: assert m.search(db,"a","Nobody") == []
def security_sql_literal(m):
    with closing(database()) as db: assert m.search(db,"a", "' OR 1=1 --") == []
def security_tenant_literal(m):
    with closing(database()) as db: assert m.search(db,"a' OR 1=1 --", "Secret") == []
def regression_apostrophe(m):
    with closing(database()) as db: assert m.search(db,"a", "O'Reilly") == [("O'Reilly",)]
def regression_case_sensitive(m):
    with closing(database()) as db: assert m.search(db,"a", "alice") == []
