@app.route("/admin/borrow/<int:request_id>", methods=["PATCH"])
@jwt_required()
def update_borrow_request(request_id):
    current_user = get_jwt_identity()
    if not current_user["is_admin"]:
        return jsonify({"msg": "Admins only"}), 403

    data = request.json
    status = data["status"]

    if status not in ["APPROVED", "DENIED"]:
        return jsonify({"msg": "Invalid status"}), 400

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE BorrowRequests SET status = %s WHERE id = %s", (status, request_id))
        conn.commit()
    finally:
        conn.close()

    return jsonify({"msg": f"Request {status.lower()}"}), 200
