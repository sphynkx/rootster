#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, render_template
import subprocess
import pymysql
from config import MYSQL_CONFIG, SECRET_KEY, PERMIT_DELETE_EXCLUDE_TABLES, EDITABLE_FIELDS
from utils import *
from db import get_db
from db.read import *
from db.delete import *
from db.edit import *

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


## Dummy - 2DEL
## Replacing with Dashboard tmp/routines
@app.route("/index")
def index():
    if "admin" not in session:
        return redirect(url_for("login"))
    all_tables = get_table_list()
    return render_template("index.html", all_tables=all_tables)


######### Dashboard routines ##############

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
######### /Dashboard routines ##############



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