import os
from flask import Flask
from flask import render_template
from flask_wtf import CSRFProtect
from util_database import db_path
from util_database import initialize_database
from util_check_user import check_user
from route_list_articles import route_list_articles
from route_create_article import route_create_article
from route_view_article import route_view_article
from route_edit_article import route_edit_article
from route_owner_login import route_owner_login
from route_delete_article import route_delete_article
from route_search_article import route_search_article
from route_owner_panel import route_owner_panel
from route_register import route_register
from route_login import route_login
from route_logout import route_logout
from route_delete_comment import route_delete_comment
ROOT = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.secret_key = "Some_Blog_Made_With_Flask"
app.config["article_images"] = os.path.join(ROOT, "static", "article_images")
csrf = CSRFProtect(app)
app.register_blueprint(route_list_articles)
app.register_blueprint(route_create_article)
app.register_blueprint(route_view_article)
app.register_blueprint(route_edit_article)
app.register_blueprint(route_owner_login)
app.register_blueprint(route_delete_article)
app.register_blueprint(route_search_article)
app.register_blueprint(route_owner_panel)
app.register_blueprint(route_register)
app.register_blueprint(route_login)
app.register_blueprint(route_logout)
app.register_blueprint(route_delete_comment)

@app.errorhandler(Exception)
def handle_exception(error):
    user_data = check_user()
    response = f"We have encountered an unexpected situation ! Error : {error}."
    return render_template("page_response.html",
                           response = response,
                           user=user_data[0],
                           is_owner=user_data[1])
if __name__ == "__main__":
    initialize_database(db_path)
    app.run(debug=True,host="0.0.0.0")
