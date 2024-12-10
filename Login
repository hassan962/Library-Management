@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Users WHERE email = %s", (email,))
        user = cursor.fetchone()

    if not user or not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity={"id": user["id"], "is_admin": user["is_admin"]})
    return jsonify({"token": token})
