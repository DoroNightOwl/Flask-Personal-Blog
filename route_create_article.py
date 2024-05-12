from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session 
from flask import current_app
from flask import flash
from util_database import db_path
from util_database import ROOT
from util_check_user import check_user
from datetime import datetime
import sqlite3
import uuid
import os
route_create_article = Blueprint("route_create_article", __name__)
@route_create_article.route("/create_article", methods=["GET", "POST"])
def create_article():
    session = check_user()
    if session[1] == False :
        return render_template("page_response.html",
                               user=session[0])
    if request.method == "POST":
        article_id = str(uuid.uuid4())
        article_poster = request.files.get("article_poster", None)
        if not article_poster: 
            flash("You forgot to upload an article poster !")
            return redirect("/create_article")
        article_title = request.form["article_title"]
        if not article_title :
            flash("You forgot to add a title to your article !")
            return redirect("/create_article")
        article_content = request.form["article_content"]
        if not article_content :
            flash("You forgot to write some content for your article !")
            return redirect("/create_article")
        current_time = datetime.now()
        current_time = current_time.strftime("%Y-%m-%d %H:%M")
        current_time = current_time.split(" ")
        current_time[0] = current_time[0].replace("-", "/")
        if article_poster :
            image_name = f"{article_id}" + ".jpg"
            image_path = os.path.join(current_app.config["article_images"], image_name)
            article_poster.save(image_path)
            print(image_path)
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        query = "INSERT INTO articles (article_id, article_title, creation_date, creation_time, total_views, article_content) VALUES (?,?,?,?,?,?)"
        cursor.execute(query,(article_id, article_title, current_time[0], current_time[1], 0, article_content))
        db.commit()
        db.close()
        return redirect("/create_article")
    else :
        return render_template("page_create_article.html",
                               user=session[0],
                               is_owner=session[1])
