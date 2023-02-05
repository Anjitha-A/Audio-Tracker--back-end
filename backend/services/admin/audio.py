from logging import Logger
from turtle import title
from models.models import Audio
import pymysql
from config import mydb
from flask import jsonify, make_response
from flask import request
from app import app
from services.db_services import execute,closeConnection,commitConnection
from validations import validateAudioData
from services.jwt import tocken_required
from services.logger import *


# insert audio details into audio table
@app.route('/audio', methods=['POST'])
@tocken_required
def createAudio(trackid=None):
    try:
        json = request.json
        title = json['title']
        artist = json['artist']
        category = json['category']
        album = json['album']
        image = json['image']
        addAudio(trackid, title,artist, category, album, image)
        # audio = Audio(trackid, title, artist, category, album, image)
        # if title and artist and category and album and image and request.method == 'POST':
        #     # conn = mydb.connect()
        #     # cursor = conn.cursor(pymysql.cursors.DictCursor)
        #     sqlQuery = "INSERT INTO audio(title, artist, category, album, image) VALUES( %s, %s, %s,%s,%s)"
        #     bindData = (audio.title, audio.artist, audio.category, audio.album, audio.image)
        #     execute(sqlQuery, bindData)
        #     # conn.commit()
        #     commitConnection()
        #     response = jsonify('Audio added successfully!')
        #     response.status_code = 200
        #     return response
        # else:   
        #     return showMessage()
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify('Some Columns are missing or Mispelled the Column name')
    except pymysql.IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        return jsonify('You are entering wrong category id , which is not in table..!!!')
    except Exception as e :
        return jsonify('something went wrong..!!')
    return jsonify({"message":"audio added successfully"})

# delete audio from table audio
@app.route('/audio/<trackid>', methods=['DELETE'])
@tocken_required
def deleteAudio(trackid, title=None, artist=None,  category=None, album=None, image=None):
    try:
        # conn = mydb.connect()
        # cursor = conn.cursor(pymysql.cursors.DictCursor)
        audio = Audio(trackid, title, artist, category, album, image)
        sqlQuery = "SELECT title FROM audio WHERE trackid =%s"
        bindData = audio.trackid
        data = execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            # conn.commit()
            commitConnection()
            response = jsonify('Audio does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM audio WHERE trackid =%s"
            bindData = audio.trackid
            data = execute(sqlQuery, bindData)
            print(data)
            # conn.commit()
            commitConnection()
            respone = jsonify('this audio deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
            print(e)
            return jsonify("error")
# updae audio from audio table
@app.route('/audio/<trackid>', methods=['PUT'])
@tocken_required
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
            # conn = mydb.connect()
            # cursor = conn.cursor(pymysql.cursors.DictCursor)
            query = "SELECT title FROM audio WHERE trackid=%s"
            bindData = audio.trackid
            data = execute(query, bindData)
            if data == 0:
                # conn.commit()
                commitConnection()
                response = jsonify('Audio does not exist')
                return response
            elif data == 1:
                sqlQuery = " UPDATE audio SET title= %s, artist= %s, category= %s, album= %s, image=%s  WHERE trackid=%s "
                bindData = (audio.title, audio.artist, audio.category, audio.album, audio.image, audio.trackid)
                execute(sqlQuery, bindData)
                # conn.commit()
                commitConnection()
                respone = jsonify('Audio updated successfully!')
                respone.status_code = 200
                print(respone)
                return respone
        else:
            return jsonify('something went wrong')
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify('Some Columns are missing or Mispelled the Column name')
    except pymysql.IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        return jsonify('You are entering wrong category id , which is not in table..!!!')
    except Exception as e:
        return jsonify('some error')
# view all audios from audio table
@app.route('/audio', methods=['GET'])
@tocken_required
def viewAudios():
    try:   
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
      
        cursor.execute("SELECT audio.trackid, audio.title, audio.artist, category.category, audio.album, audio.image , rating.rating FROM audio JOIN category ON audio.category = category.categoryid JOIN rating ON audio.trackid = rating.trackid;")
        empRows = cursor.fetchall()
        conn.commit()
        # commitConnection()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
        return jsonify("error")
        
# view particular audio from audio table

@app.route('/audio/<trackid>', methods=['GET'])
@tocken_required
def audioDetails(trackid, title=None, artist=None, category=None, album=None, image=None):
    try:
        audio = Audio(trackid, title, artist, category, album, image)
        print(audio.trackid)
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # query = "SELECT rating.rating FROM trackid=%s"
        # bind = audio.trackid
        # cursor.execute(query, bind)
        #sqlQuery = "SELECT audio.trackid, audio.title, audio.artist, category.category, audio.album, audio.image  FROM audio JOIN category ON audio.category = category.categoryid WHERE trackid= %s"
        sqlQuery = "SELECT * FROM (SELECT audio.trackid,audio.title,audio.album, audio.image,audio.artist,category.category,  avg(rating.rating) from rating inner join audio on audio.trackid = rating.trackid inner join category on audio.category = category.categoryid group by audio.title,audio.category , audio.image,audio.album,audio.trackid) sub where trackid = %s";
        bindData = audio.trackid
        cursor.execute(sqlQuery, bindData)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
        return jsonify("error")

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
  



  #for testing we are writting the code as seperate file
def addAudio(trackid, title, artist, category, album, image):
        if not title or not artist or not category or not album or not image:
            response = make_response(jsonify({'message': 'All fields are required'}))
            response.status_code = 400
            return response
        audio = Audio(trackid, title, artist, category, album, image)
        if request.method == 'POST':
            sqlQuery = "INSERT INTO audio(title, artist, category, album, image) VALUES( %s, %s, %s,%s,%s)"
            bindData = (audio.title, audio.artist, audio.category, audio.album, audio.image)
            try:
                execute(sqlQuery, bindData)
                commitConnection()
                response = jsonify({'message': 'audio added successfully!'})
                response.status_code = 200
                return response
            except pymysql.err.IntegrityError as e:
                logger.error(f"IntegrityError: {e}")
                return jsonify({'message': 'Audio already exists with the same name'})
            
        
            




