import csv
from flask import send_file

@app.route("/user/export", methods=["GET"])
@jwt_required()
def export_history():
    current_user = get_jwt_identity()
    user_id = current_user["id"]

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT b.title, br.start_date, br.end_date, br.status FROM BorrowRequests br "
            "JOIN Books b ON br.book_id = b.id WHERE br.user_id = %s", 
            (user_id,)
        )
        history = cursor.fetchall()

    filename = f"borrow_history_{user_id}.csv"
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Start Date", "End Date", "Status"])
        for row in history:
            writer.writerow([row["title"], row["start_date"], row["end_date"], row["status"]])

    return send_file(filename, as_attachment=True)
