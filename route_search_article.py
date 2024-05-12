from flask import Blueprint
from flask import request
from flask import render_template
from flask import flash
import sqlite3
from util_check_user import check_user
from util_database import db_path

route_search_article = Blueprint("route_search_article", __name__)
@route_search_article.route("/search_article", methods=["GET", "POST"])
def search_article():
    session = check_user()
    if request.method == "POST" :
        search_critera = request.form["search_criteria"]
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        query = "SELECT * FROM articles WHERE article_content MATCH ?"
        cursor.execute(query,(search_critera,))
        searched_articles = cursor.fetchall()
        if len(searched_articles) == 0 :
            response = "We were not able to find any articles matching your criteria !"
        else :
            response = f'We found {len(searched_articles)} results that match the "{search_critera}" criteria.'
        return render_template("page_search_article.html",
                               user=session[0],
                               is_owner=session[1],
                               searched_articles=searched_articles,
                               response = response)
    return render_template("page_search_article.html",
                            user=session[0],
                            is_owner=session[1])

    

