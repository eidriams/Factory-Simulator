import sqlite3 as sql
from machine import Machine
from datetime import datetime


conn = sql.connect("factory.db")
cursor = conn.cursor()

def create_table():
# include current cycle, error cycles, queues
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS machine_data (
        cycle INTEGER,
        machine TEXT,
        status TEXT,
        production INTEGER,
        errors_count INTEGER,
        error_cycles INTEGER,
        maintenance_type TEXT,
        timestamp TEXT
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS simulation_data (
        cycle INTEGER,
        queue_1 INTEGER,
        queue_2 INTEGER,
        created_pieces INTEGER,
        completed_pieces INTEGER
        )
    """)

    conn.commit()

def insert_data(machine,cycle):

    cursor.execute("""
    INSERT INTO machine_data VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,(
        cycle,
        machine.name,
        machine.status,
        machine.production_count,
        machine.errors_count,
        machine.error_cycles,
        machine.maintenance_type,
        datetime.now().replace(microsecond=0)
    ))

    conn.commit()

def insert_simulation_data(
    cycle,
    queue_1,
    queue_2,
    created_pieces,
    completed_pieces):

    cursor.execute("""
    INSERT INTO simulation_data VALUES (?, ?, ?, ?, ?)
    """,(
        cycle,
        queue_1,
        queue_2,
        created_pieces,
        completed_pieces))
    
    conn.commit()


def reset_db():

    cursor.execute("""
    DROP TABLE machine_data
    """)

    cursor.execute("""
    DROP TABLE simulation_data
    """)

    conn.commit()
    conn.close()