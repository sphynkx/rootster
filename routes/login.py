from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app as app
from db.read import check_admin

login_bp = Blueprint('login', __name__)


@login_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if check_admin(username, password):
            session["admin"] = username
            return redirect(url_for("dashboard_stat.dashboard"))
        else:
            flash("Incorrect login or password!!")
    return render_template("login.html")


@login_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("login.login"))

