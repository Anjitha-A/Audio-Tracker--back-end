

from urllib import response
from models import Rating
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app

#add rating for a particular track by particular user, datas are added to table rating
@app.route('/rating', methods = ['POST'])
def addRating(rateid=None):
    try:
        json = request.json
        userid = json['userid']
        trackid = json['trackid']
        rating = json['rating']
        print(json)
        rateobj = Rating(rateid,userid, trackid, rating)
        if userid and trackid and rating and request.method == 'POST' :
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO rating(userid, trackid, rating) VALUES (%s, %s, %s)"
            bindData = (rateobj.userid, rateobj.trackid, rateobj.rating)
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify('Rating added successfully!')
            response.status_code = 200
            return response
    except KeyError:
        return jsonify('value missing')
    except pymysql.IntegrityError as e:
        return jsonify('You are entering wrong userid or trackid , which is not in table..!!!')
    except Exception as e :
        print(e)
#view rating of particular song 
# @app.route('/rating/<trackid>', methods = ['GET'])
# def viewRating(trackid,userid=None,rating=None,rateid=None):
#     try:
#         conn = mydb.connect()
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#         rateobj = Rating(rateid,userid, trackid, rating)
#         sqlQuery = "SELECT rating.rating,audio.title FROM rating JOIN audio  ON rating.trackid = audio.trackid WHERE trackid= %s"
#         bindData = rateobj.trackid
#         cursor.execute(sqlQuery,bindData)
#         conn.commit()
#         response = jsonify('Rating added successfully!')
#         response.status_code = 200
#         return response
#     except Exception as e :
#         print(e)

