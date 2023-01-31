
import json
import bcrypt
from models import User,Rating
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from validations import validateRegisterData,validateLoginData
from db_services import execute,closeConnection,commitConnection
# registration of user, here datas are entered to user table
@app.route('/register', methods=['POST'])
def register(userid=None):
    try:
        json = request.json
        fullname = json['fullname']
        username = json['username']
        password = json['password']
        usertype = "2"
        validation_error = validateRegisterData(fullname, username, password)
        if validation_error:
            return validation_error
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(hashed_password)
        user = User (userid, fullname, username, hashed_password, usertype)
        if fullname and username and password and usertype and request.method == 'POST' :
            # conn = mydb.connect()
            # cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT fullname FROM user WHERE username= %s"
            bindData = user.username
            data = execute(query, bindData)
            #data will return 1 when the query excecutes successfully and return 0 when no such record is found
            if(data == 1):
                # conn.commit()
                commitConnection()
                return jsonify('Usre already exist !!')
            elif (data == 0):
                sqlQuery = "INSERT INTO user(fullname, username, password, usertype) VALUES( %s, %s, %s, %s)"
                bindData = (user.fullname, user.username, user.password, user.usertype)
                execute(sqlQuery, bindData)
                # conn.commit()
                commitConnection()
                respone = jsonify('User added successfully!')
                respone.status_code = 200
                return respone
        else:
            return jsonify("something went wrong")
    except KeyError:
        return jsonify(' Some Columns are missing or Mispelled the Column name')
    except Exception as e :
        print(e)

# login function of user
@app.route('/login', methods = ['POST'])
def login(userid=None, fullname=None, usertype=None):
    try: 
        json = request.json
        username = json['username']
        password = json['password']
        validation_error = validateLoginData( username, password)
        if validation_error:
            return validation_error
        user = User (userid, fullname, username, password, usertype)
        if username and password and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM user WHERE username= %s"
            bindData = user.username
            data = cursor.execute(query, bindData)
            if(data == 1):
                row = cursor.fetchone()
                hashed_password = row.get('password')
                usertype = row.get('usertype')
                if ( bcrypt.checkpw(user.password.encode('utf-8'),hashed_password.encode('utf-8'))):
                    access_token = jwt.encode({'username': username}, app.config['JWT_SECRET_KEY'])
                    conn.commit()
                    return jsonify(message='Login Successful', access_token=access_token ,usertype=usertype),200
                else:
                    conn.commit()
                    return jsonify('Password is incorrect, Try with the correct one..!!')
            else:
                conn.commit()
                return jsonify('Bad email or Password... Access Denied!'), 401
    except KeyError:
        return jsonify(' Some Columns are missing or Mispelled the Column name')
    except Exception as e :
        print(e)


