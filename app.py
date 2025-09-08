#!/usr/bin/python
from flask import Flask
from config import SECRET_KEY
from utils import inject_config


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.context_processor(inject_config)


from routes.login import login_bp
from routes.dashboard_sys import dashboard_sys_bp
from routes.dashboard_stat import dashboard_stat_bp
from routes.table_view import table_view_bp

app.register_blueprint(login_bp)
app.register_blueprint(dashboard_sys_bp)
app.register_blueprint(dashboard_stat_bp)
app.register_blueprint(table_view_bp)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port="5000")

