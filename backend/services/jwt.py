import jwt
from app import app
from functools import wraps
from flask import jsonify,request
def tocken_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        access_token =request.headers.get('Authorization')
        print(access_token)
        access_token = access_token.replace('Bearer ', '')
        if not access_token:
            return jsonify({"alert":"Token is missing..!!"})
        try:
            jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms='HS256')
           
        except:
            return jsonify({"alert":"Invalid Token"})  
        return func(*args, **kwargs)
    return decorated