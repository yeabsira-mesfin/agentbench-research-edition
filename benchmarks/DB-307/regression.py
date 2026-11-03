def search(db, tenant, name):
    return db.execute("SELECT name FROM records WHERE tenant = ? AND lower(name) = lower(?)", (tenant, name)).fetchall()
