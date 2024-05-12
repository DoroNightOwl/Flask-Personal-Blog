from flask import Blueprint
from flask import flash
from flask import request
from flask import session
from flask import render_template
PASSWORD = "Zimbabwe@69"
USERNAME = "admin"

route_owner_login = Blueprint("route_owner_login", __name__)
@route_owner_login.route("/owner_login", methods=["GET", "POST"])
def owner_login():
    if request.method=="POST":
        owner_username = request.form["owner_username"]
        owner_password = request.form["owner_password"]
        if owner_username == USERNAME and owner_password == PASSWORD :
            session["is_owner"] = True
            session["user"] = owner_username
            flash("You have been logged in as the site administrator !")
            print("Owner confirmed !")
    return render_template("page_owner_login.html")