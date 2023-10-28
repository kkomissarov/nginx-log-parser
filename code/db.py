import os
from contextlib import contextmanager

import psycopg2
from dataclasses import asdict

from dto import LogData


@contextmanager
def db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host='db',
        port=5432
    )
    try:
        yield conn
    finally:
        conn.close()


def insert_logs_bulk(logs: list[LogData]):
    sql = """
        INSERT INTO nginx_logs (
            hash, created, ip, method, url, response_code, response_size, referer, user_agent
        )
        VALUES (
            %(hash)s, 
            %(created)s, 
            %(ip)s, 
            %(method)s, 
            %(url)s, 
            %(response_code)s, 
            %(response_size)s, 
            %(referer)s, 
            %(user_agent)s
        )
        ON CONFLICT (hash) DO NOTHING;
    """

    logs_as_dicts = [asdict(log) for log in logs]

    with db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(sql, logs_as_dicts)
        conn.commit()
