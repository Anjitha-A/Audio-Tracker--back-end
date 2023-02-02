from models import Role
from flask import jsonify
from flask import request
from app import app
import pymysql
from config import mydb
from services.db_services import execute,closeConnection,commitConnection
from services.jwt import tocken_required
from services.logger import *
@app.route('/add_role', methods=['POST'])
@tocken_required
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
        
    except KeyError:
        return jsonify('key error, one value is missing')
    except pymysql.IntegrityError as e:
        logger.error(f"IntegrityError: {e}")
        return jsonify('You are entering wrong category id , which is not in table..!!!')
    except Exception as e :
        return jsonify('something went wrong..!!')

