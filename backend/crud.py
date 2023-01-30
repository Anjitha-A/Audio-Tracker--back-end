import bcrypt
from models import Category,Audio,Role,User
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from db_services import execute,closeConnection,commitConnection

        
# insert categories of audios to category table
@app.route('/category', methods=['POST'])
def addCategory(categoryid=None):
    try:
        json = request.json
        category = json['category']
        categoryobj = Category(categoryid, category)
        if category and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO category(category) VALUES( %s)"
            bindData = categoryobj.category
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify('Category is added successfully')
            response.status_code = 200
            return response
        else:
            return "something went wrong"
    except KeyError:
        return jsonify('key error, one value is missing')
    
# delete a particular category from category table
@app.route('/category/<categoryid>', methods=['DELETE'])
def deleteCategory(categoryid, category=None):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        categoryobj = Category(categoryid, category)
        sqlQuery = "SELECT category FROM category WHERE categoryid =%s"
        bindData = categoryobj.categoryid
        data = cursor.execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            conn.commit()
            response = jsonify('Category does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM category WHERE categoryid =%s"
            bindData = categoryobj.categoryid
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            respone = jsonify('this category deleted successfully!')
            respone.status_code = 200
            return respone
    except :
            return jsonify('something went wrong')

# insert audio details into audio table
@app.route('/audio', methods=['POST'])
def createAudio(trackid=None):
    try:
        json = request.json
        print(json)
        title = json['title']
        artist = json['artist']
        category = json['category']
        album = json['album']
        image = json['image']
        audio = Audio(trackid, title, artist, category, album, image)
        if title and artist and category and album and image and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO audio(title, artist, category, album, image) VALUES( %s, %s, %s,%s,%s)"
            bindData = (audio.title, audio.artist, audio.category, audio.album, audio.image)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Audio added successfully!')
            response.status_code = 200
            return response
        else:   
            return showMessage()
    except KeyError as e:
        return jsonify('key error, one value is missing')
    except Exception as e :
        return jsonify('something went wrong..!!')

# delete audio from table audio
@app.route('/audio/<trackid>', methods=['DELETE'])
def deleteAudio(trackid, title=None, artist=None,  category=None, album=None, image=None):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        audio = Audio(trackid, title, artist, category, album, image)
        sqlQuery = "SELECT title FROM audio WHERE trackid =%s"
        bindData = audio.trackid
        data = cursor.execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            conn.commit()
            response = jsonify('Audio does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM audio WHERE trackid =%s"
            bindData = audio.trackid
            data = cursor.execute(sqlQuery, bindData)
            print(data)
            conn.commit()
            respone = jsonify('this audio deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
            print(e)
# updae audio from audio table
@app.route('/audio/<trackid>', methods=['PUT'])
def updateAudio(trackid):
    try:
        _json = request.json
        print(_json)
        new_track_id = trackid
        new_title = _json['title']
        new_artist = _json['artist']
        new_category = _json['category']
        new_album = _json['album']
        new_image = _json['image']
        audio = Audio(new_track_id, new_title, new_artist, new_category, new_album, new_image)
        print(audio.trackid)
        if new_title and new_artist and new_category and new_album and new_image and request.method == 'PUT':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT title FROM audio WHERE trackid=%s"
            bindData = audio.trackid
            data = cursor.execute(query, bindData)
            if data == 0:
                conn.commit()
                response = jsonify('Audio does not exist')
                return response
            elif data == 1:
                sqlQuery = " UPDATE audio SET title= %s, artist= %s, category= %s, album= %s, image=%s  WHERE trackid=%s "
                bindData = (audio.title, audio.artist, audio.category, audio.album, audio.image, audio.trackid)
                cursor.execute(sqlQuery, bindData)
                conn.commit()
                respone = jsonify('Audio updated successfully!')
                respone.status_code = 200
                print(respone)
                return respone
        else:
            return jsonify('One value is missing..  All fields are mandatory')
    except KeyError:
        return jsonify('One value is missing..  All fields are mandatory')
# view all audios from audio table
@app.route('/audio', methods=['GET'])
def viewAudios():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT audio.trackid, audio.title, audio.artist, category.category, audio.album, audio.image FROM audio JOIN category ON audio.category = category.categoryid;")
        empRows = cursor.fetchall()
        conn.commit()
        # commitConnection()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
        
# view particular audio from audio table
@app.route('/audio/<trackid>', methods=['GET'])
def audioDetails(trackid, title=None, artist=None, category=None, album=None, image=None):
    try:
        audio = Audio(trackid, title, artist, category, album, image)
        print(audio.trackid)
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT audio.trackid, audio.title, audio.artist, category.category, audio.album, audio.image FROM audio JOIN category ON audio.category = category.categoryid WHERE trackid= %s"
        bindData = audio.trackid
        cursor.execute(sqlQuery, bindData)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
# add values to role table
@app.route('/add_role', methods=['POST'])
def addRole(roleid=None):
    try:
        json = request.json
        role = json['role']
        roleobj = Role(roleid, role)
        if role and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO role(role) VALUES( %s)"
            bindData = roleobj.role
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify('Category is added successfully')
            response.status_code = 200
            return response
        else:
            return "something went wrong"
    except KeyError:
        return jsonify('key error, one value is missing')

# registration of user, here datas are entered to user table
@app.route('/register', methods=['POST'])
def register(userid=None):
    try:
        json = request.json
        fullname = json['fullname']
        username = json['username']
        password = json['password']
        usertype = "2"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(hashed_password)
        user = User (userid, fullname, username, hashed_password, usertype)
        if fullname and username and password and usertype and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO user(fullname, username, password, usertype) VALUES( %s, %s, %s, %s)"
            bindData = (user.fullname, user.username, user.password, user.usertype)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            return jsonify(status='success', message='User registered successfully')
        else:
            return "something went wrong"
    except KeyError:
        return jsonify('key error, one value is missing')
    
# error handling
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
  
# if __name__ == "__main__":
#     app.run()

