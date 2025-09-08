from flask import Blueprint, jsonify, render_template
from db.read import get_table_list
from db.stats import *
from datetime import datetime, timedelta

dashboard_stat_bp = Blueprint('dashboard_stat', __name__)


@dashboard_stat_bp.route('/dashboard')
def dashboard():
    all_tables = get_table_list()
    top10_users = [row['user_id'] for row in get_top10_users()]
    top10_books = [row['bookname_ru'] for row in get_top10_books()]
    return render_template('dashboard.html',
                          all_tables=all_tables,
                          top10_users=top10_users,
                          top10_books=top10_books
    )


@dashboard_stat_bp.route('/dashboard/api/stats/summary')
def dashboard_stats_summary():
    total_users = get_total_users()
    active_users = get_active_users()
    if total_users > 0:
        active_percent = int(active_users / total_users * 100)
    else:
        active_percent = 10
    min_delay, max_delay, avg_delay = get_request_time_stats()
    ru_percent, en_percent = get_language_percent()
    return jsonify({
        "total_users": total_users,
        "active_users": active_users,
        "active_percent": round(active_users * 100 / total_users, 1) if total_users else 0,
        "request_time_min": round(min_delay, 1),
        "request_time_max": round(max_delay, 1),
        "request_time_avg": round(avg_delay, 1),
        "lang_ru_percent": ru_percent,
        "lang_en_percent": en_percent,
    })


@dashboard_stat_bp.route('/dashboard/api/stats/requests_by_day')
def requests_by_day():
    rows = get_requests_by_day()
    today = datetime.now().date()
    date_map = {str(row['day']): row['count'] for row in rows}
    days = []
    counts = []
    for i in range(7):
        d = (today - timedelta(days=6-i)).strftime("%Y-%m-%d")
        days.append(d)
        counts.append(date_map.get(d, 0))
    return jsonify({"days": days, "counts": counts})


@dashboard_stat_bp.route('/dashboard/api/stats/books_hits')
def books_hits():
    rows = get_books_hits()
    labels = [row['bookname_ru'] for row in rows]
    data = [row['hits'] for row in rows]
    return jsonify({"labels": labels, "data": data})

