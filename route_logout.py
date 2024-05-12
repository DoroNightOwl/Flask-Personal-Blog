from flask import Blueprint
from flask import session
from flask import flash
from flask import redirect
from flask import render_template
from util_check_user import check_user

route_logout = Blueprint("route_logout", __name__)
@route_logout.route("/logout")
def logout():
    is_logged = check_user()
    if is_logged[0] != None :
        session.pop("user", None)
        if is_logged[1] == True :
            session.pop("is_owner", None)
        flash("Logged out succesfully !")
        return redirect("/list_articles")

    else :
        response = "You can't log out if you are not logged in !"
        return render_template("page_response.html", response=response)

