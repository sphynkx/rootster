#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pymysql
from config import MYSQL_CONFIG, SECRET_KEY
import datetime
import hashlib


app = Flask(__name__)
app.secret_key = SECRET_KEY



def get_db():
    return pymysql.connect(**MYSQL_CONFIG, cursorclass=pymysql.cursors.DictCursor)


def check_admin(username, password):
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM admins WHERE username=%s AND is_active=1", (username,))
            admin = cursor.fetchone()
            if admin:
                pwd_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
                if admin["password_hash"] == pwd_hash:
                    # Обновляем last_login
                    cursor.execute(
                        "UPDATE admins SET last_login = %s WHERE username = %s",
                        (datetime.datetime.now(), username)
                    )
                    conn.commit()
                    return True
    finally:
        conn.close()
    return False


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_admin(username, password):
            session["admin"] = username
            return redirect(url_for("tables"))
        else:
            flash("Неверный логин или пароль")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login"))


@app.route("/tables")
def tables():
    if "admin" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [row[f"Tables_in_{MYSQL_CONFIG['database']}"] for row in cursor.fetchall()]
    finally:
        conn.close()
    return render_template("tables.html", tables=tables)


@app.route("/table/<table>")
def table_view(table):
    if "admin" not in session:
        return redirect(url_for("login"))
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM `{table}` LIMIT 100")
            rows = cursor.fetchall()
            cursor.execute(f"SHOW COLUMNS FROM `{table}`")
            columns = [col["Field"] for col in cursor.fetchall()]
    finally:
        conn.close()
    return render_template("table_view.html", table=table, rows=rows, columns=columns)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="5000")

