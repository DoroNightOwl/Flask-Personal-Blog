import sqlite3
from util_database import db_path
from util_check_user import check_user
from flask import Blueprint
from flask import session
from flask import request
from flask import render_template
from flask import flash
from flask import redirect
from datetime import datetime
import shortuuid
route_view_article = Blueprint("view_article", __name__)
@route_view_article.route("/articles/view_article/<article_id>", methods=["GET", "POST"])
def view_article(article_id):
    session = check_user()
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    query = "SELECT * FROM articles WHERE article_id=?"
    cursor.execute(query,(article_id,))
    requested_article = cursor.fetchone()
    query = "SELECT * FROM comments WHERE article_id=? ORDER BY ROWID DESC"
    cursor.execute(query,(article_id,))
    requested_comments = cursor.fetchall()
    db.commit()
    db.close()
    if request.method == "POST":
        comment_id = shortuuid.uuid()
        comment_content = request.form["comment_content"]
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        current_time = datetime.now()
        current_time = current_time.strftime("%Y-%m-%d %H:%M")
        current_time = current_time.split(" ")
        current_time[0] = current_time[0].replace("-", "/")
        query = "INSERT INTO comments (comment_id, author, creation_date, creation_time, article_id, comment_content) VALUES (?,?,?,?,?,?)"
        cursor.execute(query,(comment_id, session[0], current_time[0], current_time[1], article_id, comment_content))
        db.commit()
        db.close()
        flash("Comment successfully added !")
        return redirect(f"/articles/view_article/{article_id}")
    return render_template("page_view_article.html", 
                           requested_article=requested_article, 
                           requested_comments=requested_comments,
                           user=session[0],
                           is_owner=session[1])
