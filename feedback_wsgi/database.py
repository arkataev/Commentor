import sqlite3
import os

conn = sqlite3.connect(os.path.abspath('db.sqlite'))
cur = conn.cursor()

def get_regions():
    stmt = "Select * from regions"
    cur.execute(stmt)
    return cur.fetchall()
