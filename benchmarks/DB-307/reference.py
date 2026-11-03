def search(db, tenant, name):
    return db.execute("SELECT name FROM records WHERE tenant = ? AND name = ?", (tenant, name)).fetchall()
