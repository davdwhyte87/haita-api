from flask import jsonify,request,session
from blueprints.user.models import User
import jwt
from flask import current_app
from functools import wraps


# def decorator_function(original_function):
#     def wrapper_function():
#         print("decorator function started")
#         return original_function()
#     return wrapper_function()


# @app_.before_request
def login_required(f):
    @wraps(f)
    def authchack(*args, **kwargs):
        # get the owner of the token,check if the user exists and set the user id in session
        token=request.headers.get('Auth')
        if token:
            try:
                data=jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=['HS256'])
                # print(data)
                request.user_id=data['user_id']
                request.user_type=data['user_type']
            except Exception as err:
                print(err)
                return jsonify(code=0,message="An error occurred. Decode error")
            return f(*args, **kwargs)
        else:
            return jsonify(code=0,message="An error occured")
    return authchack

