import bcrypt
import pymysql
import json
from config import mydb
from flask import jsonify
from flask import flash, request
from app import app
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token






from email.mime import image
import pymysql
import json
from app import app
from config import mydb
from flask import jsonify
from flask import flash, request





#insert audio details into audio table
@app.route('/insert', methods=['POST'])
def create_audio():
    try:
        json = request.json
        print(json)
        # track_id= json['track_id']
        title = json['title']
        category = json['category']
        author = json['author']
        image = json['image']
        
        if title and category and author and image and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO audio(  title, category, author, image) VALUES( %s, %s, %s,%s)"
            bindData = ( title, category, author, image)
            cursor.execute(sqlQuery, bindData)
            # print(cursor.execute(sqlQuery, bindData))
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



#view all datas in table
@app.route('/view_audios', methods =['GET'])
def view_audios():
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
    finally:
        cursor.close() 
        conn.close() 



#view particular data from table
@app.route('/view_audio/<track_id>', methods=['GET'])
def audio_details(track_id):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT track_id , title, category, author, image FROM audio WHERE track_id =%s", (track_id))
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()





#update audio
@app.route('/update/<track_id>', methods=['PUT'])
def update_audio(track_id):
    try:
        _json = request.json
        print(_json)
        _track_id = track_id
        _title = _json['title']
        _category= _json['category']
        _author = _json['author']
        _image = _json['image']
       
        if  _title and _category and _author and  _image and request.method  == 'PUT':   
            sqlQuery = ("UPDATE audio SET title= %s, category= %s, author= %s, image=%s  WHERE track_id=%s")
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
    finally:
        cursor.close()
        conn.close() 

#delete track
@app.route('/delete/<track_id>', methods=['DELETE'])
def delete_audio(track_id):
    try:
        conn = mydb.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM audio WHERE track_id =%s",(track_id))
        conn.commit()
        respone = jsonify('Audio deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()




#add ratings by user
@app.route('/add_rating/<track_id>', methods=['PUT'])
def add_ratings(track_id):
    try:
        json = request.json
        print(json)
        # track_id= json['track_id']
        rating = json['rating']
        if rating and request.method == 'PUT':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "UPDATE audio SET rating=%s  WHERE track_id =%s"
            bindData = (rating,track_id)
            cursor.execute(sqlQuery, bindData)
            # print(cursor.execute(sqlQuery, bindData))
            conn.commit()
            respone = jsonify('rating added successfully!')
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









#login and signup

@app.route('/get', methods=['GET'])
def Get():
    return 'haii'

@app.route('/register', methods=['POST'])
def register():
    try:
        json = request.json
        print(json)
        email= json['email']
        username = json['username']
        password = json['password']
        usertype = "user"
        # hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # print(hashed)
      
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


@app.route('/login', methods=['POST'])
def login():
    try:
        json = request.json
        print(json)
        username = json['username']
        password = json['password']
        # login_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(username)
        if username and password and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            sqlQuery="SELECT * FROM user WHERE username= '%s'  and password='%s'" % (username, password)
            # sqlQuery="SELECT * FROM user WHERE username= '%s' " % (username)
            # print(sqlQuery)
            data=cursor.execute(sqlQuery)
            row = cursor.fetchone()
            usertype=row.get('usertype')         
            if data==1:
                access_token = create_access_token(identity=username)
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


            








@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone



@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    app.run()