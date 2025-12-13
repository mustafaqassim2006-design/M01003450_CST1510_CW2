# schema.py
from .db import DatabaseManager as DM

def create_tables(db: DM):
    c = db.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        incident_id TEXT NOT NULL UNIQUE,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        reported_at TEXT,
        resolved_at TEXT,
        assigned_to TEXT,
        description TEXT
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_name TEXT NOT NULL UNIQUE,
        owner TEXT,
        source_system TEXT,
        size_mb REAL,
        row_count INTEGER,
        created_at TEXT
    );
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT NOT NULL UNIQUE,
        category TEXT,
        priority TEXT,
        status TEXT,
        opened_at TEXT,
        closed_at TEXT,
        assigned_to TEXT
    );
    """)
