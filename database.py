import sqlite3 as sql
from machine import Machine
from datetime import datetime


conn = sql.connect("factory.db")
cursor = conn.cursor()

def create_table():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS machine_data (
        machine TEXT,
        status TEXT,
        production INTEGER,
        timestamp TEXT
        )
    """)

    conn.commit()

def insert_data(machine):

    cursor.execute("""
    INSERT INTO machine_data VALUES (?, ?, ?, ?)
    """,(
        machine.name,
        machine.status,
        machine.production_count,
        datetime.now().replace(microsecond=0)
    ))

    conn.commit()

def reset_db():

    cursor.execute("""
    DROP TABLE machine_data
    """)

    conn.commit()
    conn.close()