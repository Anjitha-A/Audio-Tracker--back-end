import json
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from db_services import execute,closeConnection, cursor
#insert audio details into audio table
@app.route('/insert', methods=['POST'])
def createAudio():
    try:
        json = request.json
        print(json)
        title = json['title']
        category = json['category']
        author = json['author']
        image = json['image']
        if title and category and author and image and request.method == 'POST':
            sqlQuery = "INSERT INTO audio( title, category, author, image) VALUES( %s, %s, %s,%s)"
            bindData = ( title, category, author, image)
            execute(sqlQuery,bindData)
            respone = jsonify('Audio added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'

#view all datas in audio table
@app.route('/view_audios', methods =['GET'])
def viewAudios():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM audio")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e: 
        print(e)
     
#view particular data from audio table
@app.route('/view_audio/<trackid>', methods=['GET'])
def audioAetails(trackid):
    try:
        sqlQuery="SELECT trackid , title, category, author, image FROM audio WHERE trackid =%s"
        bindData =(trackid)
        execute(sqlQuery,bindData)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        closeConnection()
#update audio from audio table
@app.route('/update/<trackid>', methods=['PUT'])
def updateAudio(trackid):
    try:
        _json = request.json
        print(_json)
        _track_id = trackid
        _title = _json['title']
        _category= _json['category']
        _author = _json['author']
        _image = _json['image']
       
        if  _title and _category and _author and  _image and request.method  == 'PUT':   
            sqlQuery = ("UPDATE audio SET title= %s, category= %s, author= %s, image=%s  WHERE trackid=%s")
            bindData = ( _title, _category, _author,  _image,_track_id )
            conn = mydb.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            respone = jsonify('Audio updated successfully!')
            respone.status_code = 200
            print(respone)
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
    
#delete track from audio table
@app.route('/delete/<trackid>', methods=['DELETE'])
def deleteAudio(trackid):
    try:
        sqlQuery="DELETE FROM audio WHERE trackid =%s"
        bindData=(trackid)
        execute(sqlQuery,bindData)
        respone = jsonify('Audio deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

# signup for user , with email, username and password and datas are enetered to user table
@app.route('/register', methods=['POST'])
def register():
    try:
        json = request.json
        print(json)
        email= json['email']
        username = json['username']
        password = json['password']
        usertype = "user"
        if email and username and password and usertype and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query= "SELECT * FROM user WHERE username= '%s'" % (username)
            data=cursor.execute(query)
            print(data)
            if data>0:
                conn.commit()
                response = jsonify('User already Exsist!!')
                response.status_code = 200
                return response
            else:
                sqlQuery = "INSERT INTO user(email,username,password, usertype) VALUES(%s, %s, %s , %s)"
                bindData = (email,username,password, usertype)
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                respone = jsonify('User added successfully!')
                respone.status_code = 200
                return respone      
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'
    finally:
        cursor.close()
        conn.close()
#Login function , which enable the user to login to the application using username and password
@app.route('/login', methods=['POST'])
def login():
    try:
        json = request.json
        print(json)
        username = json['username']
        password = json['password']
        print(username)
        if username and password and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery="SELECT * FROM user WHERE username= '%s'  and password='%s'" % (username, password)
            data=cursor.execute(sqlQuery)
            print(data)      
            if data==1:
                row = cursor.fetchone()
                usertype=row.get('usertype') 
                access_token = jwt.encode({
                    'username': username
                }, app.config['JWT_SECRET_KEY'])
                conn.commit()
                return jsonify(message='Login Successful', access_token=access_token ,usertype=usertype),200
            else:
                conn.commit()
                return jsonify('Bad email or Password... Access Denied!'), 401
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'
    finally:
        cursor.close()
        conn.close()  
#shows the exeption       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


closeConnection()

if __name__ == "__main__":
    app.run()
