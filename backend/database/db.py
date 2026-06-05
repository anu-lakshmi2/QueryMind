import sqlite3
import os
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'querymind.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def execute_query(query, params=()):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def execute_non_query(query, params=()):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.lastrowid
    
def execute_write(sql, params=()):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        return cursor.lastrowid