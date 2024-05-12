from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template
from flask import flash
from util_check_user import check_user
from util_database import db_path
import sqlite3
route_owner_panel = Blueprint("route_owner_panel", __name__)
@route_owner_panel.route("/owner_panel", methods=["GET","POST"])
def owner_panel():
    session = check_user()
    if session[1] == False :
        return render_template("page_response.html")
    if request.method == "POST" :
        article_id = request.form["article_id"]
        comment_id = request.form["comment_id"]
        if len(article_id) == 0 or len(comment_id) == 0 :
            flash("One or more fields are emtpy !")
            return redirect("/owner_panel")
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        query = "DELETE FROM comments WHERE article=? AND id=?"
        cursor.execute(query,(article_id, comment_id))
        affected_rows = cursor.rowcount
        db.commit()
        db.close()
        if affected_rows == 0 :
            flash("Article or comment doesn't exist ! No operation performed !")
            return redirect("/owner_panel")
        else :
            flash("Comment deleted succesfully !")
            return redirect("/owner_panel")
    return render_template("page_owner_panel.html",
                            user=session[0],
                            is_owner=session[1])

    