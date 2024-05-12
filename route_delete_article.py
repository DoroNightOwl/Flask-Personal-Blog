from flask import Blueprint
from flask import redirect
from flask import flash
from flask import render_template
from flask import current_app
import sqlite3
import os
from util_database import db_path
from util_check_user import check_user

route_delete_article = Blueprint("route_delete_article", __name__)
@route_delete_article.route("/delete_article/<article_id>", methods=["GET", "POST"])
def delete_article(article_id):
    session = check_user()
    if session[1] == False :
        return render_template("page_response.html")
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    query = "DELETE FROM articles WHERE article_id=?"
    try :
        image_name = f"{article_id}" + ".jpg"
        image_path = os.path.join(current_app.config["article_images"], image_name)
        os.remove(image_path)
        print(image_path)
    except Exception as error:
        print("An error occurred:", error)
    cursor.execute(query,(article_id,))
    db.commit()
    db.close()
    flash(f"Post with ID {article_id} has been eliminated from the database !")
    return redirect("/list_articles")