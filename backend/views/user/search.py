
from functools import wraps
from datetime import datetime, timedelta
import json
import bcrypt
from models import User
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from validations import validateRegisterData,validateLoginData
from services.db_services import execute,closeConnection,commitConnection

#searching audios by title, category or album
@app.route('/search', methods=['POST'])
def search():
    try:
        json = request.json
        search_value = json['search_value']
        print(search_value)
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print("after connection")
        cursor.execute("SELECT title FROM audio WHERE title LIKE %s OR artist LIKE %s OR album LIKE %s",(search_value,search_value,search_value))
        conn.commit()
        data = cursor.fetchall
        print("after fetch all")
        print(data)  
        if len(data) == 0 :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT name, author from Book")
            conn.commit()
            data = cursor.fetchall()

    except Exception as e:
        print(e)





# # registration of user, here datas are entered to user table
# @app.route('/register', methods=['POST'])
# def register(userid=None):
#     try:
#         json = request.json
#         fullname = json['fullname']
#         username = json['username']
#         password = json['password']
#         usertype = "2"
#         validation_error = validateRegisterData(fullname, username, password)
#         if validation_error:
#             return validation_error
#         hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#         print(hashed_password)
#         user = User (userid, fullname, username, hashed_password, usertype)
#         if fullname and username and password and usertype and request.method == 'POST' :
#             # conn = mydb.connect()
#             # cursor = conn.cursor(pymysql.cursors.DictCursor)
#             query = "SELECT fullname FROM user WHERE username= %s"
#             bindData = user.username
#             data = execute(query, bindData)
#             #data will return 1 when the query excecutes successfully and return 0 when no such record is found
#             if(data == 1):
#                 # conn.commit()
#                 commitConnection()
#                 return jsonify('Usre already exist !!')
#             elif (data == 0):
#                 sqlQuery = "INSERT INTO user(fullname, username, password, usertype) VALUES( %s, %s, %s, %s)"
#                 bindData = (user.fullname, user.username, user.password, user.usertype)
#                 execute(sqlQuery, bindData)
#                 # conn.commit()
#                 commitConnection()
#                 respone = jsonify('User added successfully!')
#                 respone.status_code = 200
#                 return respone
#         else:
#             return jsonify("something went wrong")
#     except KeyError:
#         return jsonify(' Some Columns are missing or Mispelled the Column name')
#     except Exception as e :
#         print(e)




