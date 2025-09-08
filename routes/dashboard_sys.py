from flask import Blueprint, render_template, jsonify
import subprocess
from db.read import get_table_list
from db.stats import get_top10_users, get_top10_books

dashboard_sys_bp = Blueprint('dashboard_sys', __name__)


@dashboard_sys_bp.route('/dashboard/restart_service', methods=['POST'])
def dashboard_restart_service():
    try:
        subprocess.run(['systemctl', 'restart', 'korneslov-bot.service'], check=True)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))


@dashboard_sys_bp.route('/dashboard/start_service', methods=['POST'])
def dashboard_start_service():
    try:
        subprocess.run(['systemctl', 'start', 'korneslov-bot.service'], check=True)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))


@dashboard_sys_bp.route('/dashboard/stop_service', methods=['POST'])
def dashboard_stop_service():
    try:
        subprocess.run(['systemctl', 'stop', 'korneslov-bot.service'], check=True)
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))


@dashboard_sys_bp.route('/dashboard/service_status')
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

