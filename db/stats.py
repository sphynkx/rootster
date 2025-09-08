import json
from db import get_db


def get_total_users():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total FROM users")
        row = cursor.fetchone()
    conn.close()
    return row['total'] if row else 0


def get_active_users():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(DISTINCT user_id) AS active FROM requests")
        row = cursor.fetchone()
    conn.close()
    return row['active'] if row else 0


def get_request_time_stats():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT MIN(delay) AS min_delay, MAX(delay) AS max_delay, AVG(delay) AS avg_delay FROM requests WHERE status_oai > 0")
        row = cursor.fetchone()
    conn.close()
    if row:
        min_delay = row['min_delay'] if row['min_delay'] is not None else 0
        max_delay = row['max_delay'] if row['max_delay'] is not None else 0
        avg_delay = row['avg_delay'] if row['avg_delay'] is not None else 0
    else:
        min_delay = max_delay = avg_delay = 0
    return min_delay, max_delay, avg_delay


def get_language_percent():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("SELECT user_state FROM requests")
        states = cursor.fetchall()
    conn.close()
    ru_cnt = en_cnt = 0
    for row in states:
        state_str = row['user_state'] if isinstance(row, dict) else row[0]
        if not state_str:
            continue
        try:
            ## reform string to dict
            state = json.loads(state_str)
            lang = state.get('lang')
            if lang == 'ru':
                ru_cnt += 1
            elif lang == 'en':
                en_cnt += 1
        except (json.JSONDecodeError, TypeError, KeyError):
            ## If no success..
            continue
    total = ru_cnt + en_cnt
    if total == 0:
        return 0, 0
    return ru_cnt * 100 // total, en_cnt * 100 // total


def get_requests_by_day():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT DATE(datetime_request) AS day, COUNT(*) AS count
            FROM requests
            WHERE datetime_request >= CURDATE() - INTERVAL 6 DAY
            GROUP BY day
            ORDER BY day
        """)
        rows = cursor.fetchall()
    conn.close()
    return rows


def get_books_hits():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT bookname_ru, hits FROM books -- replace with `bookname_en` to view eng booknames
            WHERE hits > 0 -- remove to get all books in legend
            ORDER BY hits DESC
            -- LIMIT 15 -- optional limit for hitted books.. mabe no need
        """)
        rows = cursor.fetchall()
    conn.close()
    return rows


def get_top10_users():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT user_id
            FROM requests
            GROUP BY user_id
            ORDER BY COUNT(*) DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
    conn.close()
    return rows


def get_top10_books():
    conn = get_db()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT bookname_ru
            FROM books
            ORDER BY hits DESC
            LIMIT 10
        """)
        rows = cursor.fetchall()
    conn.close()
    return rows
