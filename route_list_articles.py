from flask import Blueprint
from flask import session
from flask import render_template
from flask import current_app
from util_database import db_path
from util_check_user import check_user
import sqlite3
import os
route_list_articles = Blueprint("route_list_articles", __name__)
@route_list_articles.route("/list_articles")
def home_page():
    session = check_user()
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    query = "SELECT * FROM articles ORDER BY ROWID DESC"
    cursor.execute(query)
    requested_articles = cursor.fetchall()
    db.commit()
    db.close()
    return render_template("page_list_articles.html", 
                            requested_articles=requested_articles,
                            user = session[0],
                            is_owner = session[1],
                            os=os)