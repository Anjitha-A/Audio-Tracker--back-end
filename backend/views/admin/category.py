from models import Category
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
            # conn = mydb.connect()
            # cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO category(category) VALUES( %s)"
            bindData = categoryobj.category
            execute(sqlQuery,bindData)
            # conn.commit()
            commitConnection()
            response = jsonify('Category is added successfully')
            response.status_code = 200
            return response
        else:
            return "something went wrong"
    except KeyError:
        return jsonify('One value is missing..  All fields are mandatory')
    
# delete a particular category from category table
@app.route('/category/<categoryid>', methods=['DELETE'])
def deleteCategory(categoryid, category=None):
    try:
        # conn = mydb.connect()
        # cursor = conn.cursor(pymysql.cursors.DictCursor)
        categoryobj = Category(categoryid, category)
        sqlQuery = "SELECT category FROM category WHERE categoryid =%s"
        bindData = categoryobj.categoryid
        data = execute(sqlQuery, bindData)
        print(data)
        if data == 0:
            # conn.commit()
            commitConnection()
            response = jsonify('Category does not exist')
            return response
        elif data == 1:
            sqlQuery = "DELETE FROM category WHERE categoryid =%s"
            bindData = categoryobj.categoryid
            execute(sqlQuery,bindData)
            # conn.commit()
            commitConnection()
            respone = jsonify('this category deleted successfully!')
            respone.status_code = 200
            return respone
    except Exception as e:
        print(e)
        return jsonify('something went wrong')