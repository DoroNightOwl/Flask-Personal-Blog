from flask import Blueprint
from flask import flash
from flask import redirect
from flask import request
from flask import render_template
import sqlite3
import bcrypt
from util_database import db_path
from util_check_user import check_user

email_domains = ["@gmail.com", "@yahoo.com"]
route_register = Blueprint("route_register", __name__)
@route_register.route("/register", methods=["GET", "POST"])
def register():
    session = check_user()
    print(session[0])
    if session[0] != None :
        response="You are already logged in !"
        return render_template("page_response.html", response=response)
    elif request.method == "POST" :
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if len(username) == 0  or len(email) == 0  or len(password) == 0  or len(confirm_password) == 0 :
            flash("One or more fields are emtpy !")
            return redirect("/register")
        if len(password) < 8 : 
            flash("Your password must have at least 8 characters !")
            return redirect("/register")
        if password != confirm_password :
            flash('"Password" and "Confirm Password" fields do not match !')
            return redirect("/register")
        valid_email = False
        for i in range(len(email_domains)) :
            if email.find(email_domains[i]) != (-1) :
                valid_email = True
                break
        if valid_email == False :
            flash("Your email address is not valid !")
            return redirect("/register")
        db = sqlite3.connect(db_path)
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username=?"
        cursor.execute(query,(username,))
        print("DOG : ",cursor.rowcount)
        if cursor.rowcount != (-1)  :
            flash(f'Username "{username}" is already in use !')
            db.commit()
            db.close()
            return redirect("/register")
        query = "SELECT * FROM users WHERE email=?"
        cursor.execute(query,(username,))
        if cursor.rowcount != (-1):
            flash(f'Email "{email}" is already in use !')
            db.commit()
            db.close()
            return redirect("/register")
        query = "INSERT INTO users (username, email, password) VALUES (?,?,?)"
        salt = bcrypt.gensalt()
        cursor.execute(query,(username, email, bcrypt.hashpw(password.encode("utf-8"), salt)))
        db.commit()
        db.close()
        flash("Account created successfully !")
        return redirect("/register")
    else :
        return render_template("page_register.html",
                               user=session[0],
                               is_owner=session[1])


        

        
        

            
