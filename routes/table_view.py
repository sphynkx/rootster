from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from db.read import get_table_list, get_table_rows_and_columns
from db.delete import delete_response_and_request, delete_request_and_response, delete_row_from_table
from db.edit import edit_row_handler
from config import PERMIT_DELETE_EXCLUDE_TABLES, EDITABLE_FIELDS

table_view_bp = Blueprint('table_view', __name__)


@table_view_bp.route("/table/<table>")
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


@table_view_bp.route("/delete_response/<int:response_id>", methods=["POST"])
def delete_response(response_id):
    if "admin" not in session:
        return {"success": False, "error": "Not authorized"}, 403
    result = delete_response_and_request(response_id)
    return {"success": bool(result)}


@table_view_bp.route("/delete_request/<int:request_id>", methods=["POST"])
def delete_request(request_id):
    if "admin" not in session:
        return {"success": False, "error": "Not authorized"}, 403
    result = delete_request_and_response(request_id)
    return {"success": bool(result)}


## Deletes record from any 
@table_view_bp.route("/delete_generic/<table>/<int:row_id>", methods=["POST"])
def delete_generic(table, row_id):
    if "admin" not in session:
        return {"success": False, "error": "Not authorized"}, 403

    ok = delete_row_from_table(table, row_id, PERMIT_DELETE_EXCLUDE_TABLES)
    if ok:
        return {"success": True}
    return {"success": False, "error": "Table not allowed"}, 400


@table_view_bp.route('/edit_row/<table>/<int:row_id>', methods=['POST'])
def edit_row(table, row_id):
    data = request.get_json()
    return edit_row_handler(table, row_id, data)

