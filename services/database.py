import os
import sqlite3
from services.models import HealthReport

DB_PATH = os.path.join("data", "history.db")


def init_db() -> None:
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checked_at TEXT,
            total INTEGER,
            ok INTEGER,
            failed INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            check_id INTEGER,
            name TEXT,
            url TEXT,
            status TEXT,
            http_code INTEGER,
            response_time_ms INTEGER,
            error TEXT,
            FOREIGN KEY (check_id) REFERENCES checks(id)
        )
    """)
    conn.commit()
    conn.close()


def save_report(report: HealthReport) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO checks (checked_at, total, ok, failed) VALUES (?, ?, ?, ?)",
        (report.checked_at, report.summary["total"], report.summary["ok"], report.summary["failed"])
    )
    check_id = cursor.lastrowid
    for r in report.results:
        cursor.execute(
            "INSERT INTO results (check_id, name, url, status, http_code, response_time_ms, error) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (check_id, r.name, r.url, r.status, r.http_code, r.response_time_ms, r.error)
        )
    conn.commit()
    conn.close()