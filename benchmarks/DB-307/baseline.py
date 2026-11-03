def search(db, tenant, name):
    return db.execute(f"SELECT name FROM records WHERE tenant = '{tenant}' AND name = '{name}'").fetchall()
