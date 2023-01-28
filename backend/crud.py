import json
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
#creating a class named Audio
class Audio:
    def __init__(self, trackid: str, title: str, category: str, author: str, image: str):
        self.trackid = trackid
        self.title = title
        self.category = category
        self.author = author
        self.image = image
# creating a class named User
class User:
    def __init__(self, userid: str, fullname: str, username: str, password: str, usertype: str):
        self.userid = userid
        self.fullname = fullname
        self.username = username
        self.password = password
        self.usertype = usertype
# insert audio details into table
@app.route('/insert', methods=['POST'])
def createAudio(trackid=None):
    try:
        json = request.json
        print(json)
        title = json['title']
        category = json['category']
        author = json['author']
        image = json['image']
        audio = Audio(trackid, title, category, author, image)
        if title and category and author and image and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO audio(title, category, author, image) VALUES( %s, %s, %s,%s)"
            bindData = (audio.title, audio.category, audio.author, audio.image)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Audio added successfully!')
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
# view all datas from audio table
@app.route('/view_audios', methods=['GET'])
def viewAudios():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM audio")
        empRows = cursor.fetchall()
        conn.commit()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
# view particular data from table
@app.route('/view_audio/<trackid>', methods=['GET'])
def audioDetails(trackid, title=None, category=None, author=None, image=None):
    try:
        audio = Audio(trackid, title, category, author, image)
        print(audio.trackid)
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT trackid , title, category, author, image FROM audio WHERE trackid =%s"
        bindData = audio.trackid
        cursor.execute(sqlQuery, bindData)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
# update audio details of a particular track which is specified by track id
@app.route('/update/<trackid>', methods=['PUT'])
def updateAudio(trackid):
    try:
        _json = request.json
        print(_json)
        new_track_id = trackid
        new_title = _json['title']
        new_category = _json['category']
        new_author = _json['author']
        new_image = _json['image']
        audio = Audio(new_track_id, new_title, new_category, new_author, new_image)
        print(audio.trackid)
        if new_title and new_category and new_author and new_image and request.method == 'PUT':
            sqlQuery = " UPDATE audio SET title= %s, category= %s, author= %s, image=%s  WHERE trackid=%s "
            bindData = (audio.title, audio.category, audio.author, audio.image, audio.trackid)
            conn = mydb.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Audio updated successfully!')
            respone.status_code = 200
            print(respone)
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
# delete particular track
@app.route('/delete/<trackid>', methods=['DELETE'])
def deleteAudio(trackid, title=None, category=None, author=None, image=None):
    try:
        audio = Audio(trackid, title, category, author, image)
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT title FROM audio WHERE trackid =%s"
        bindData = audio.trackid
        data = cursor.execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            response = jsonify('Audio does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM audio WHERE trackid =%s"
            bindData = audio.trackid
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Audio deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
        print(e)
# # signup for user , with email, username and password and datas are entered to user table
@app.route('/register', methods=['POST'])
def register(userid=None):
    try:
        json = request.json
        print(json)
        fullname = json['fullname']
        username = json['username']
        password = json['password']
        usertype = 'user'
        user = User(userid, fullname, username, password, usertype)
        if fullname and username and password and usertype and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT * FROM user WHERE username= %s"
            bindData = user.username
            data = cursor.execute(query, bindData)
            print(data)
            if data > 0:
                response = jsonify('User already Exist!!')
                response.status_code = 200
                return response
            else:
                sqlQuery = "INSERT INTO user(fullname,username,password, usertype) VALUES(%s, %s, %s , %s)"
                bindData = (user.fullname, user.username, user.password, user.usertype)
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
# Login function , which enable the user to login to the application using username and password
@app.route('/login', methods=['POST'])
def login(userid=None, fullname=None, usertype=None):
    try:
        json = request.json
        print(json)
        username = json['username']
        password = json['password']
        user = User(userid, fullname, username, password, usertype)
        print(username)
        if username and password and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "SELECT usertype FROM user WHERE username= '%s'  and password='%s'" % (user.username, user.password)
            data = cursor.execute(sqlQuery)
            print(data)
            if data == 1:
                row = cursor.fetchone()
                print(row)
                usertype = row.get('usertype')
                access_token = jwt.encode({
                    'username': username
                }, app.config['JWT_SECRET_KEY'])
                conn.commit()
                return jsonify(message='Login Successful', access_token=access_token, usertype=usertype), 200
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
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
#running the app
if __name__ == "__main__":
    app.run()
