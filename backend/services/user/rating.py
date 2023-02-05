from urllib import response
from models.models import Rating
import jwt
import pymysql
from config import mydb
from flask import jsonify
from flask import request
from app import app
from validations import validateRating
from services.jwt import tocken_required
from services.logger import *

#add rating for a particular track by particular user, datas are added to table rating
@app.route('/rating', methods = ['POST'])
@tocken_required
def addRating(rateid=None):
    try:
        json = request.json
        userid = json['userid']
        trackid = json['trackid']
        rating = json['rating']
        print(json)
        error = validateRating(rating)
        if error :
            return error
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
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify('any one of the value is missing')
    except pymysql.IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        return jsonify('You are entering wrong userid or trackid , which is not in table..!!!')
    except Exception as e :
        print(e)





# SELECT title, artist, avg(rating) 
# FROM new_db.audio join new_db.rating on audio.trackid = rating.trackid
# where audio.trackid = 4 
# group by title, artist, rating



# SELECT avg(rating) FROM new_db.rating where trackid= 4;




# select * from (select audio.title, audio.category, audio.trackid, avg(rating.rating)from new_db.rating inner join new_db.audio on audio.trackid = rating.trackid group by audio.title, audio.category,audio.trackid) sub where trackid= 4



# SELECT * FROM (select audio.title,category.category, audio.trackid, avg(rating.rating) from new_db.rating inner join new_db.audio on audio.trackid = rating.trackid inner join new_db.category on audio.category = category.categoryid group by audio.title,audio.category , audio.trackid) sub where trackid = 4;