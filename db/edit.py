from flask import jsonify
from db import get_db, EDITABLE_FIELDS, PERMIT_DELETE_EXCLUDE_TABLES



def edit_row_handler(table, row_id, data):
    if table in PERMIT_DELETE_EXCLUDE_TABLES:
        return jsonify(success=False, error="Editing not allowed for this table.")

    editable_fields = EDITABLE_FIELDS.get(table, [])
    updates = {}
    for key in data:
        if key in editable_fields:
            updates[key] = data[key]
    if not updates:
        return jsonify(success=False, error="No valid fields to update.")

    set_clause = ", ".join(f"`{k}`=%s" for k in updates)
    sql = f"UPDATE `{table}` SET {set_clause} WHERE id=%s"
    params = list(updates.values()) + [row_id]

    try:
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        conn.commit()
        conn.close()
        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

