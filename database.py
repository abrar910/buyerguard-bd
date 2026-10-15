"""
database.py - SQLite Database Management for BuyerGuard BD
Handles table initialization, indexing, connection management,
and parameterized data queries.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_FILE = os.environ.get("BUYERGUARD_DB", os.path.join(os.path.dirname(__file__), "buyerguard.db"))


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Return a configured SQLite database connection with row factory."""
    path = db_path or DB_FILE
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[str] = None) -> None:
    """Create schema tables and indexes if they do not exist."""
    conn = get_db_connection(db_path)
    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS plots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plot_id TEXT UNIQUE NOT NULL,
                demo_district TEXT NOT NULL,
                demo_upazila TEXT NOT NULL,
                demo_mouza_code TEXT NOT NULL,
                khatian_ref TEXT,
                deed_ref TEXT,
                mutation_status TEXT,
                case_info_status TEXT,
                khas_acquisition_status TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plot_id TEXT NOT NULL,
                transaction_ref TEXT NOT NULL,
                deed_ref TEXT,
                transaction_type TEXT NOT NULL,
                transaction_date TEXT NOT NULL,
                record_status TEXT NOT NULL,
                conflict_group_id TEXT,
                FOREIGN KEY (plot_id) REFERENCES plots(plot_id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_plots_plot_id ON plots(plot_id);
            CREATE INDEX IF NOT EXISTS idx_plots_khatian ON plots(khatian_ref);
            CREATE INDEX IF NOT EXISTS idx_plots_deed ON plots(deed_ref);
            CREATE INDEX IF NOT EXISTS idx_plots_mouza ON plots(demo_mouza_code);
            CREATE INDEX IF NOT EXISTS idx_transactions_plot_id ON transactions(plot_id);
            CREATE INDEX IF NOT EXISTS idx_transactions_conflict ON transactions(conflict_group_id);
        """)
    conn.close()


def get_all_plots(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieve all synthetic plots with basic summary info."""
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM plots ORDER BY plot_id ASC")
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_plot_by_id(plot_id: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Fetch single plot by normalized plot_id."""
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM plots WHERE UPPER(plot_id) = UPPER(?)", (plot_id.strip(),))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_transactions_for_plot(plot_id: str, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Fetch all transaction records associated with a plot."""
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM transactions 
            WHERE UPPER(plot_id) = UPPER(?) 
            ORDER BY transaction_date DESC, id DESC
        """, (plot_id.strip(),))
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def search_plots(query: str, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Search plots by plot_id, khatian_ref, deed_ref, or demo_mouza_code.
    Uses parameterized LIKE queries for safe matching.
    """
    conn = get_db_connection(db_path)
    try:
        cur = conn.cursor()
        cleaned = query.strip()
        pattern = f"%{cleaned}%"
        cur.execute("""
            SELECT * FROM plots 
            WHERE plot_id LIKE ? 
               OR khatian_ref LIKE ? 
               OR deed_ref LIKE ? 
               OR demo_mouza_code LIKE ?
               OR demo_district LIKE ?
               OR demo_upazila LIKE ?
            ORDER BY plot_id ASC
        """, (pattern, pattern, pattern, pattern, pattern, pattern))
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
