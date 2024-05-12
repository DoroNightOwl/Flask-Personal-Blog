from flask import Blueprint
from flask import flash
from flask import redirect
import sqlite3
from util_database import db_path
from util_check_user import check_user

route_delete_comment = Blueprint("route_delete_comment", __name__)
@route_delete_comment.route("/article/<article_id>/delete_comment/<comment_id>", methods=["GET", "POST"])
def delete_comment(article_id, comment_id):
    user_data = check_user()
    if user_data[1] == True :
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        query = "DELETE FROM comments WHERE article_id=? AND comment_id=?"
        cursor.execute(query,(article_id, comment_id))
        db.commit()
        db.close()
        flash(f"Comment with ID {comment_id} has been eliminated successfully !")
        return redirect(f"/articles/view_article/{article_id}")
    
