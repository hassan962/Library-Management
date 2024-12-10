@app.route("/borrow", methods=["POST"])
@jwt_required()
def borrow_request():
    current_user = get_jwt_identity()
    user_id = current_user["id"]

    data = request.json
    book_id = data["book_id"]
    start_date = data["start_date"]
    end_date = data["end_date"]

    if datetime.strptime(end_date, "%Y-%m-%d") < datetime.strptime(start_date, "%Y-%m-%d"):
        return jsonify({"msg": "Invalid date range"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT COUNT(*) AS conflict 
                   FROM BorrowRequests 
                   WHERE book_id = %s AND status = 'APPROVED' 
                   AND ((start_date <= %s AND end_date >= %s) OR 
                        (start_date <= %s AND end_date >= %s))""",
                (book_id, start_date, start_date, end_date, end_date),
            )
            conflict = cursor.fetchone()["conflict"]

            if conflict:
                return jsonify({"msg": "Book already borrowed during this period"}), 400

            cursor.execute(
                "INSERT INTO BorrowRequests (user_id, book_id, start_date, end_date) VALUES (%s, %s, %s, %s)",
                (user_id, book_id, start_date, end_date),
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify({"msg": "Borrow request submitted"}), 201
