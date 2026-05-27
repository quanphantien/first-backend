import os
from typing import Optional
from psycopg2 import sql
from psycopg2 import pool
import psycopg2

_pool: Optional[pool.ThreadedConnectionPool] = None


def init_db():
    global _pool
    if _pool is not None:
        return
    host = os.getenv("PGHOST")
    user = os.getenv("PGUSER")
    port = int(os.getenv("PGPORT", "5432"))
    dbname = os.getenv("PGDATABASE")
    password = os.getenv("PGPASSWORD")

    _pool = psycopg2.pool.ThreadedConnectionPool(1, 10,
                                                 host=host,
                                                 user=user,
                                                 password=password,
                                                 port=port,
                                                 dbname=dbname)

    # ensure table exists
    conn = _pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL
                )
                """
            )
            conn.commit()
    finally:
        _pool.putconn(conn)


def close_pool():
    global _pool
    if _pool is None:
        return
    _pool.closeall()
    _pool = None


def create_user(name: str) -> dict:
    if _pool is None:
        raise RuntimeError("DB pool is not initialized")
    conn = _pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id, name", (name,))
            row = cur.fetchone()
            conn.commit()
            return {"id": row[0], "name": row[1]}
    finally:
        _pool.putconn(conn)


def get_user(user_id: int) -> Optional[dict]:
    if _pool is None:
        raise RuntimeError("DB pool is not initialized")
    conn = _pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            return {"id": row[0], "name": row[1]}
    finally:
        _pool.putconn(conn)
