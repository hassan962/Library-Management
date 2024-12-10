@app.route("/books", methods=["GET"])
@jwt_required()
def list_books():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Books")
        books = cursor.fetchall()
    conn.close()
    return jsonify(books)
