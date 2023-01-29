import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
# create a class Category which have the details of categories of songs
class Category:
    def __init__(self, categoryid: str, category: str):
        self.categoryid = categoryid
        self.category = category
# creating a class Audio which have all the audio details
class Audio:
    def __init__(self, trackid: str, title: str, artist: str, category: int, album: str, image: str):
        self.trackid = trackid
        self.title = title
        self.artist = artist
        self.category = category
        self.album = album
        self.image = image
# create role class
class Role:
    def __init__(self, roleid: str, role: str):
        self.roleid = roleid
        self.role = role
# insert categories of audios to category table
@app.route('/insert_category', methods=['POST'])
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
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            response = jsonify('Category is added successfully')
            response.status_code = 200
            return response
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'exception'
    finally:
        cursor.close()
        conn.close()
# delete a particular category from category table
@app.route('/delete_category/<categoryid>', methods=['DELETE'])
def deleteCategory(categoryid, category=None):
    try:
        categoryobj = Category(categoryid, category)
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT category FROM category WHERE categoryid =%s"
        bindData = categoryobj.categoryid
        data = cursor.execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            response = jsonify('Category does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM category WHERE categoryid =%s"
            bindData = categoryobj.categoryid
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('this category deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
            print(e)

# insert audio details into audio table
@app.route('/insert_audio', methods=['POST'])
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
    except Exception as e:
        print(e)
        return 'Exception'
    finally:
        cursor.close()
        conn.close()
# delete audio from table audio
@app.route('/delete_audio/<trackid>', methods=['DELETE'])
def deleteAudio(trackid, title=None, artist=None,  category=None, album=None, image=None):
    try:
        audio = Audio(trackid, title, artist, category, album, image)
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
            respone = jsonify('this audio deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
            print(e)
# update audio from audio table
@app.route('/update_audio/<trackid>', methods=['PUT'])
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
            query = "SELECT title FROM audio WHERE trackid=%s"
            bindData = audio.trackid
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            data = cursor.execute(query, bindData)
            if data == 0:
                response = jsonify('Audio does not exist')
                return response
            elif data == 1:
                sqlQuery = " UPDATE audio SET title= %s, artist= %s, category= %s, album= %s, image=%s  WHERE trackid=%s "
                bindData = (audio.title, audio.artist, audio.category, audio.album, audio.image, audio.trackid)
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
# view all audios from audio table
@app.route('/view_audios', methods=['GET'])
def viewAudios():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT audio.trackid, audio.title, audio.artist, category.category, audio.album, audio.image FROM audio JOIN category ON audio.category = category.categoryid;")
        empRows = cursor.fetchall()
        conn.commit()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
# view particular audio from audio table
@app.route('/view_audio/<trackid>', methods=['GET'])
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
    finally:
        cursor.close()
        conn.close()

# add values to role table
@app.route('/add_role', methods=['POST'])
def addRole(roleid=None):
    try:
        json = request.json
        role = json['role']
        roleobj = Role(roleid, role)
        if roleid and role and request.method == ['POST']:
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO role(role) VALUES( %s)"
            bindData = roleobj.role
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('role added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'exception'
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
# running the app
if __name__ == "__main__":
    app.run()

