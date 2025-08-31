#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from config import MYSQL_CONFIG, SECRET_KEY
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


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="5000")