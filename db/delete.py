from db import get_db


def delete_response_and_request(response_id):
    """
    Deletes record from `responses` and appropriate record from `requests` (if exists). Via responses's `request_id`.
    """
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            ## Find the bound `request_id`
            cursor.execute(
                "SELECT request_id FROM responses WHERE id = %s", (response_id,)
            )
            row = cursor.fetchone()
            if row:
                request_id = row["request_id"]
            else:
                request_id = None

            ## Delete response
            cursor.execute(
                "DELETE FROM responses WHERE id = %s", (response_id,)
            )

            ## Delete bound request (if found)
            if request_id:
                cursor.execute(
                    "DELETE FROM requests WHERE id = %s", (request_id,)
                )

            conn.commit()
            return True
    finally:
        conn.close()


def delete_request_and_response(request_id):
    """
    Deletes record from `requests` and bound `response` (if exists).
    """
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            ## Delete bound `response` (if exists)
            cursor.execute(
                "DELETE FROM responses WHERE request_id = %s", (request_id,)
            )

            ## Delete `request`
            cursor.execute(
                "DELETE FROM requests WHERE id = %s", (request_id,)
            )

            conn.commit()
            return True
    finally:
        conn.close()



def delete_row_from_table(table: str, row_id: int, exclude_tables: set) -> bool:
    """
    Deletes record with defined `row_id` from any tables except `requests`, `responses` and  specified in the `exclude_tables` (see `PERMIT_DELETE_EXCLUDE_TABLES` param in config).
    Returns True if success, or False if table is permitted to deletion.
    """
    if table in exclude_tables:
        return False
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM `{table}` WHERE id = %s", (row_id,))
            conn.commit()
        return True
    finally:
        conn.close()



