#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from config import MYSQL_CONFIG, SECRET_KEY, PERMIT_DELETE_EXCLUDE_TABLES
from db import get_db
from db.read import *
from db.delete import *

app = Flask(__name__)
app.secret_key = SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_admin(username, password):
            session["admin"] = username
            return redirect(url_for("index"))
        else:
            flash("Incorrect login or password!!")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


@app.route("/index")
def index():
    if "admin" not in session:
        return redirect(url_for("login"))
    all_tables = get_table_list()
    return render_template("index.html", all_tables=all_tables)


@app.route("/table/<table>")
def table_view(table):
    if "admin" not in session:
        return redirect(url_for("login"))
    all_tables = get_table_list()
    rows, columns = get_table_rows_and_columns(table)
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
    from db.delete import delete_request_and_response
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



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="5000")