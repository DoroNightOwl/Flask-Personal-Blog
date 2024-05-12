from flask import Blueprint
from flask import request
from flask import flash
from flask import redirect
from flask import session
from flask import render_template
import sqlite3
from util_database import db_path
from util_check_user import check_user

route_edit_article = Blueprint("route_edit_article", __name__)
@route_edit_article.route("/edit_article/<article_id>", methods=["GET", "POST"])
def edit_article(article_id):
    session = check_user()
    if session[1] == False :
        return render_template("page_response.html",
                               user=session[0])
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    query = "SELECT * FROM articles WHERE article_id=?"
    cursor.execute(query,(article_id,))
    requested_article = cursor.fetchone()
    db.commit()
    db.close()
    if request.method == "POST":
        article_title = request.form["article_title"]
        article_content = request.form["article_content"]
        if not article_title :
            flash("Title field is empty !")
            return redirect(f"/edit_article/{article_id}")
        if not article_content :
            flash("You have removed your article's content entirely !")
            flash("If you want to remove this article, use the DELETE button instead !")
            return redirect(f"/edit_article/{article_id}")
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        query = "UPDATE articles SET article_title=?, article_content=? WHERE article_id=?"
        cursor.execute(query, (article_title, article_content, article_id))
        db.commit()
        db.close()
        flash("Article successfuly updated !")
        return redirect(f"/articles/view_article/{article_id}")
    return render_template("page_edit_article.html", 
                           requested_article=requested_article,
                           user=session[0],
                           is_owner=session[1])