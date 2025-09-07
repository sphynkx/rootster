#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, render_template
from datetime import datetime, timedelta
import subprocess
import pymysql
from config import MYSQL_CONFIG, SECRET_KEY, PERMIT_DELETE_EXCLUDE_TABLES, EDITABLE_FIELDS
from utils import *
from db import get_db
from db.read import *
from db.delete import *
from db.edit import *
from db.stats import *


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.context_processor(inject_config)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_admin(username, password):
            session["admin"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Incorrect login or password!!")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))



######### Dashboard sys-routines ##############

@app.route('/dashboard')
def dashboard():
    all_tables = get_table_list()
    return render_template('dashboard.html', all_tables=all_tables)


@app.route('/dashboard/restart_service', methods=['POST'])
def dashboard_restart_service():
    try:
        subprocess.run(['systemctl', 'restart', 'korneslov-bot.service'], check=True)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))


@app.route('/dashboard/start_service', methods=['POST'])
def dashboard_start_service():
    try:
        subprocess.run(['systemctl', 'start', 'korneslov-bot.service'], check=True)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))


@app.route('/dashboard/stop_service', methods=['POST'])
def dashboard_stop_service():
    try:
        subprocess.run(['systemctl', 'stop', 'korneslov-bot.service'], check=True)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))


@app.route('/dashboard/service_status')
def dashboard_service_status():
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', 'korneslov-bot.service'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        status = result.stdout.strip()
        return jsonify(status=status)
    except Exception as e:
        return jsonify(status="error")
######### /Dashboard sys-routines ##############


######### Dashboard stat-routines ##############
@app.route('/dashboard/api/stats/summary')
def dashboard_stats_summary():
    total_users = get_total_users()
    active_users = get_active_users()
    if total_users > 0:
        active_percent = int(active_users / total_users * 100)
    else:
        active_percent = 10
    min_delay, max_delay, avg_delay = get_request_time_stats()
    ru_percent, en_percent = get_language_percent()
    ##print(f" {min_delay=} , {max_delay=} , {avg_delay=}" )
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


@app.route('/dashboard/api/stats/requests_by_day')
def requests_by_day():
    rows = get_requests_by_day()
    today = datetime.datetime.now().date()
    date_map = {str(row['day']): row['count'] for row in rows}
    days = []
    counts = []
    for i in range(7):
        d = (today - timedelta(days=6-i)).strftime("%Y-%m-%d")
        days.append(d)
        counts.append(date_map.get(d, 0))
    return jsonify({"days": days, "counts": counts})


@app.route('/dashboard/api/stats/books_hits')
def books_hits():
    rows = get_books_hits()
    labels = [row['bookname_ru'] for row in rows]
    data = [row['hits'] for row in rows]
    return jsonify({"labels": labels, "data": data})


######### /Dashboard stat-routines ##############



@app.route("/table/<table>")
def table_view(table):
    if "admin" not in session:
        return redirect(url_for("login"))
    all_tables = get_table_list()
    rows, columns = get_table_rows_and_columns(table)
## 2DEL - Unactual 
##    for row in rows:
##        if table == "responses" and 'data' in row:
##            row['data'] = protect_user_paragraphs(row['data'])
    return render_template(
        "table_view.html",
        all_tables=all_tables,
        table=table,
        rows=rows,
        columns=columns
    )


@app.route("/delete_response/<int:response_id>", methods=["POST"])
def delete_response(response_id):
    if "admin" not in session:
        return {"success": False, "error": "Not authorized"}, 403
    result = delete_response_and_request(response_id)
    return {"success": bool(result)}


@app.route("/delete_request/<int:request_id>", methods=["POST"])
def delete_request(request_id):
    if "admin" not in session:
        return {"success": False, "error": "Not authorized"}, 403
    result = delete_request_and_response(request_id)
    return {"success": bool(result)}


## Deletes record from any 
@app.route("/delete_generic/<table>/<int:row_id>", methods=["POST"])
def delete_generic(table, row_id):
    if "admin" not in session:
        return {"success": False, "error": "Not authorized"}, 403

    ok = delete_row_from_table(table, row_id, PERMIT_DELETE_EXCLUDE_TABLES)
    if ok:
        return {"success": True}
    return {"success": False, "error": "Table not allowed"}, 400


@app.route('/edit_row/<table>/<int:row_id>', methods=['POST'])
def edit_row(table, row_id):
    data = request.get_json()
    return edit_row_handler(table, row_id, data)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="5000")