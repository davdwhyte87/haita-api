from flask import jsonify,request,session
from blueprints.user.models import Token
from blueprints.admin.models import AdminToken
from functools import wraps

def admin_login_required(f):
    @wraps(f)
    def authchack(*args, **kwargs):
        # get the owner of the token,check if the user exists and set the user id in session
        token=request.headers.get('Auth')
        if token:
            tk=AdminToken.query.filter_by(api_token=token).first()
            if not tk:
                return jsonify(code=0,message="The user does not exists")
            else:
                #set the user id in session
                session['admin_id']=tk.admin_id
                return f(*args, **kwargs)
        else:
            return jsonify(code=0,message="An error occured")
    return authchack