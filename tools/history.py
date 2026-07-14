import sqlite3
import json
from pathlib import Path

DB_PATH = Path("data/review_history.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        language TEXT,
        score INTEGER,
        code TEXT,
        result_json TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_review(language, score, code, result):
    conn = get_connection()

    conn.execute("""
    INSERT INTO reviews
    (language, score, code, result_json)
    VALUES (?, ?, ?, ?)
    """,
    (
        language,
        score,
        code,
        json.dumps(result)
    ))

    conn.commit()
    conn.close()


def get_recent_reviews(limit=20):
    conn = get_connection()

    rows = conn.execute("""
    SELECT
        id,
        created_at,
        language,
        score
    FROM reviews
    ORDER BY id DESC
    LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "created_at": row[1],
            "language": row[2],
            "score": row[3]
        }
        for row in rows
    ]


def get_review(review_id):
    conn = get_connection()

    row = conn.execute("""
    SELECT
        id,
        created_at,
        language,
        score,
        code,
        result_json
    FROM reviews
    WHERE id = ?
    """, (review_id,)).fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "created_at": row[1],
        "language": row[2],
        "score": row[3],
        "code": row[4],
        "result": json.loads(row[5])
    }