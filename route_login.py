from flask import Blueprint
from flask import render_template
from flask import flash
from flask import redirect
from flask import request
from flask import session
import sqlite3
import bcrypt
from util_check_user import check_user
from util_database import db_path

route_login = Blueprint("route_login", __name__)
@route_login.route("/login", methods=["GET", "POST"])
def login():
    session_user_data = check_user()
    if session_user_data[0] != None :
        flash("You are already logged in !")
        return render_template("page_response.html",
                               user = session_user_data[0],
                               is_owner = session_user_data[1])
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) == 0 or len(password) == 0 :
            flash("One or more fields are emtpy !")
            return redirect("/login")
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username=?"
        cursor.execute(query,(username,))
        requested_user = cursor.fetchone()
        print("FUCKTHARD " , requested_user)
        if requested_user == None :
            flash(f'Account with username "{username}" does not exist !')
            return redirect("/login")
        db.commit()
        db.close()
        password_bytes = password.encode("utf-8")
        given_password = requested_user[2]
        if bcrypt.checkpw(password_bytes, given_password) :
            session["user"] = username
            flash("Logged in successfully !")
            return redirect("/list_articles")
        else :
            flash("Incorrect password !")
            return redirect("/login")
    return render_template("page_login.html",
                           user = session_user_data[0],
                           is_owner = session_user_data[1])


