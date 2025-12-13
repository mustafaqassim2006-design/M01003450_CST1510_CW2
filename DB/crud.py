# crud.py
from __future__ import annotations

import sqlite3
from typing import Any, Optional, Tuple


# ---------------------------
# Small DB helpers
# ---------------------------

def _get_conn(db: Any) -> Optional[sqlite3.Connection]:
    """
    Supports either:
      - sqlite3.Connection
      - an object that has .conn (sqlite3.Connection)
    """
    if isinstance(db, sqlite3.Connection):
        return db
    return getattr(db, "conn", None)


def _cursor(db: Any) -> sqlite3.Cursor:
    """
    Supports either sqlite3.Connection or a DB manager with .cursor().
    """
    if isinstance(db, sqlite3.Connection):
        return db.cursor()
    return db.cursor()


def _commit(db: Any) -> None:
    """
    Commit if we can. Safe to call even if DB manager commits elsewhere.
    """
    conn = _get_conn(db)
    if conn is not None:
        conn.commit()


# ---------------------------
# USERS
# ---------------------------

def insert_user(db: Any, username: str, password_hash: str, role: str) -> Tuple[bool, str]:
    """
    Requires users.username to be UNIQUE in schema.
    Returns (success, message).
    """
    c = _cursor(db)
    try:
        c.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role),
        )
        _commit(db)
        return True, f"User '{username}' created."
    except sqlite3.IntegrityError:
        return False, f"Username '{username}' already exists."


def get_user_by_username(db: Any, username: str):
    c = _cursor(db)
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    return c.fetchone()


# ---------------------------
# CYBER INCIDENTS
# ---------------------------

def incident_exists(db: Any, incident_id: str) -> bool:
    c = _cursor(db)
    c.execute("SELECT 1 FROM cyber_incidents WHERE incident_id = ? LIMIT 1", (incident_id,))
    return c.fetchone() is not None


def create_incident(
    db: Any,
    incident_id: str,
    incident_type: str,
    severity: str,
    status: str,
    reported_at: str,
    resolved_at: str,
    assigned_to: str,
    description: str,
) -> Tuple[bool, str]:
    """
    Requires cyber_incidents.incident_id to be UNIQUE in schema.
    Returns (success, message).
    """
    c = _cursor(db)
    try:
        c.execute(
            """
            INSERT INTO cyber_incidents
            (incident_id, incident_type, severity, status, reported_at, resolved_at, assigned_to, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (incident_id, incident_type, severity, status, reported_at, resolved_at, assigned_to, description),
        )
        _commit(db)
        return True, f"Incident '{incident_id}' created."
    except sqlite3.IntegrityError:
        return False, f"Incident ID '{incident_id}' already exists."


def get_all_incidents(db: Any):
    c = _cursor(db)
    c.execute("SELECT * FROM cyber_incidents")
    return c.fetchall()


def update_incident_status(db: Any, incident_id: str, new_status: str) -> Tuple[bool, str]:
    c = _cursor(db)
    c.execute(
        """
        UPDATE cyber_incidents
        SET status = ?
        WHERE incident_id = ?
        """,
        (new_status, incident_id),
    )
    _commit(db)
    if c.rowcount == 0:
        return False, f"No incident found with ID '{incident_id}'."
    return True, f"Incident '{incident_id}' updated."


def delete_incident(db: Any, incident_id: str) -> Tuple[bool, str]:
    c = _cursor(db)
    c.execute("DELETE FROM cyber_incidents WHERE incident_id = ?", (incident_id,))
    _commit(db)
    if c.rowcount == 0:
        return False, f"No incident found with ID '{incident_id}'."
    return True, f"Incident '{incident_id}' deleted."


# ---------------------------
# DATASETS METADATA
# ---------------------------

def dataset_exists(db: Any, dataset_name: str) -> bool:
    c = _cursor(db)
    c.execute("SELECT 1 FROM datasets_metadata WHERE dataset_name = ? LIMIT 1", (dataset_name,))
    return c.fetchone() is not None


def create_dataset(
    db: Any,
    dataset_name: str,
    owner: str,
    source_system: str,
    size_mb: float,
    row_count: int,
    created_at: str,
) -> Tuple[bool, str]:
    """
    Requires datasets_metadata.dataset_name to be UNIQUE in schema.
    Returns (success, message).
    """
    c = _cursor(db)
    try:
        c.execute(
            """
            INSERT INTO datasets_metadata
            (dataset_name, owner, source_system, size_mb, row_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (dataset_name, owner, source_system, size_mb, row_count, created_at),
        )
        _commit(db)
        return True, f"Dataset '{dataset_name}' created."
    except sqlite3.IntegrityError:
        return False, f"Dataset name '{dataset_name}' already exists."


def get_all_datasets(db: Any):
    c = _cursor(db)
    c.execute("SELECT * FROM datasets_metadata")
    return c.fetchall()


def update_dataset_owner(db: Any, dataset_name: str, new_owner: str) -> Tuple[bool, str]:
    c = _cursor(db)
    c.execute(
        """
        UPDATE datasets_metadata
        SET owner = ?
        WHERE dataset_name = ?
        """,
        (new_owner, dataset_name),
    )
    _commit(db)
    if c.rowcount == 0:
        return False, f"No dataset found with name '{dataset_name}'."
    return True, f"Dataset '{dataset_name}' updated."


def delete_dataset(db: Any, dataset_name: str) -> Tuple[bool, str]:
    c = _cursor(db)
    c.execute("DELETE FROM datasets_metadata WHERE dataset_name = ?", (dataset_name,))
    _commit(db)
    if c.rowcount == 0:
        return False, f"No dataset found with name '{dataset_name}'."
    return True, f"Dataset '{dataset_name}' deleted."


# ---------------------------
# IT TICKETS
# ---------------------------

def ticket_exists(db: Any, ticket_id: str) -> bool:
    c = _cursor(db)
    c.execute("SELECT 1 FROM it_tickets WHERE ticket_id = ? LIMIT 1", (ticket_id,))
    return c.fetchone() is not None


def create_ticket(
    db: Any,
    ticket_id: str,
    category: str,
    priority: str,
    status: str,
    opened_at: str,
    closed_at: str,
    assigned_to: str,
) -> Tuple[bool, str]:
    """
    Requires it_tickets.ticket_id to be UNIQUE in schema.
    Returns (success, message).
    """
    c = _cursor(db)
    try:
        c.execute(
            """
            INSERT INTO it_tickets
            (ticket_id, category, priority, status, opened_at, closed_at, assigned_to)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (ticket_id, category, priority, status, opened_at, closed_at, assigned_to),
        )
        _commit(db)
        return True, f"Ticket '{ticket_id}' created."
    except sqlite3.IntegrityError:
        return False, f"Ticket ID '{ticket_id}' already exists."


def get_all_tickets(db: Any):
    c = _cursor(db)
    c.execute("SELECT * FROM it_tickets")
    return c.fetchall()


def update_ticket_status(db: Any, ticket_id: str, new_status: str) -> Tuple[bool, str]:
    c = _cursor(db)
    c.execute(
        """
        UPDATE it_tickets
        SET status = ?
        WHERE ticket_id = ?
        """,
        (new_status, ticket_id),
    )
    _commit(db)
    if c.rowcount == 0:
        return False, f"No ticket found with ID '{ticket_id}'."
    return True, f"Ticket '{ticket_id}' updated."


def delete_ticket(db: Any, ticket_id: str) -> Tuple[bool, str]:
    c = _cursor(db)
    c.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    _commit(db)
    if c.rowcount == 0:
        return False, f"No ticket found with ID '{ticket_id}'."
    return True, f"Ticket '{ticket_id}' deleted."
