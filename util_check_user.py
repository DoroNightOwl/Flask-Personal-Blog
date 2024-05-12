from flask import session
def check_user():
    if "user" in session : user = session["user"]
    else : user = None
    if "is_owner" in session : is_owner = session["is_owner"]
    else : is_owner = False
    return (user, is_owner)