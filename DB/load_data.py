# load_data.py
from pathlib import Path
import pandas as pd
from .db import DatabaseManager

DATA_DIR = Path("DATA")

# table -> primary-key-like column
PK_COL = {
    "cyber_incidents": "incident_id",
    "datasets_metadata": "dataset_name",
    "it_tickets": "ticket_id",
}

def _get_existing_keys(db: DatabaseManager, table: str, pk_col: str) -> set[str]:
    c = db.cursor()
    c.execute(f"SELECT {pk_col} FROM {table}")
    return {row[0] for row in c.fetchall() if row[0] is not None}

def load_csv_to_table(db: DatabaseManager, csv_path: Path, table_name: str) -> tuple[int, int]:
    """
    Returns: (inserted_count, skipped_count)
    Skips rows where PK already exists in DB, and warns in console.
    """
    if not csv_path.exists():
        print(f"Skipping {csv_path.name}, file not found")
        return 0, 0

    df = pd.read_csv(csv_path)

    pk = PK_COL.get(table_name)
    if not pk:
        # fallback: just append (but ideally all your domain tables should be in PK_COL)
        df.to_sql(table_name, db.conn, if_exists="append", index=False)
        print(f"Loaded {len(df)} rows into {table_name}")
        return len(df), 0

    # Drop rows with missing PK (cannot load safely)
    before = len(df)
    df = df.dropna(subset=[pk])
    if len(df) != before:
        print(f"⚠ {table_name}: dropped {before - len(df)} rows with missing {pk}")

    # Remove duplicates inside the CSV itself
    before = len(df)
    df = df.drop_duplicates(subset=[pk], keep="first")
    csv_dupes = before - len(df)
    if csv_dupes:
        print(f"⚠ {table_name}: {csv_dupes} duplicate {pk} values inside CSV were ignored")

    existing = _get_existing_keys(db, table_name, pk)
    mask_new = ~df[pk].astype(str).isin({str(x) for x in existing})

    skipped = int((~mask_new).sum())
    df_new = df[mask_new]

    if skipped:
        print(f"⚠ {table_name}: skipped {skipped} rows because {pk} already exists in DB")

    if not df_new.empty:
        df_new.to_sql(table_name, db.conn, if_exists="append", index=False)
        print(f"✔ Loaded {len(df_new)} new rows into {table_name}")
    else:
        print(f"✔ No new rows to load into {table_name}")

    return len(df_new), skipped

def load_all_csv_data(db: DatabaseManager):
    mapping = {
        "cyber_incidents.csv": "cyber_incidents",
        "datasets_metadata.csv": "datasets_metadata",
        "it_tickets.csv": "it_tickets",
    }

    total_inserted = 0
    total_skipped = 0

    for filename, table in mapping.items():
        path = DATA_DIR / filename
        ins, skp = load_csv_to_table(db, path, table)
        total_inserted += ins
        total_skipped += skp

    print(f"\nCSV load summary: inserted={total_inserted}, skipped(existing)={total_skipped}")
