from db import get_db

def delete_response_and_request(response_id):
    """
    Удаляет запись из responses и соответствующий запрос из requests.
    Если связанного запроса нет — просто удаляет response.
    """
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Найти связанный request_id
            cursor.execute(
                "SELECT request_id FROM responses WHERE id = %s", (response_id,)
            )
            row = cursor.fetchone()
            if row:
                request_id = row["request_id"]
            else:
                request_id = None

            # Удалить response
            cursor.execute(
                "DELETE FROM responses WHERE id = %s", (response_id,)
            )

            # Удалить связанный request, если найден
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
    Удаляет запись из requests и связанный response, если такой есть.
    Если ответа нет — просто удаляет request.
    """
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            # Удалить связанный response, если есть
            cursor.execute(
                "DELETE FROM responses WHERE request_id = %s", (request_id,)
            )

            # Удалить request
            cursor.execute(
                "DELETE FROM requests WHERE id = %s", (request_id,)
            )

            conn.commit()
            return True
    finally:
        conn.close()