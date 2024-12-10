@app.route("/admin/users", methods=["POST"])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    if not current_user["is_admin"]:
        return jsonify({"msg": "Admins only"}), 403

    data = request.json
    name = data["name"]
    email = data["email"]
    password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    is_admin = data.get("is_admin", False)

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Users (name, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)",
                (name, email, password, is_admin),
            )
        conn.commit()
    except pymysql.err.IntegrityError:
        return jsonify({"msg": "Email already exists"}), 400
    finally:
        conn.close()

    return jsonify({"msg": "User created"}), 201
