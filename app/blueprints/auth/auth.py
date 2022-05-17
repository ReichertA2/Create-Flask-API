from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.blueprints.api.models import User
# from .models import *
from flask import g

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(email, password):
    #check to see if the user even exists
    u = User.query.filter_by(email=email).first()
    if u is None:
        return False
    g.current_user = u
    return u.check_hashed_password(password)

    