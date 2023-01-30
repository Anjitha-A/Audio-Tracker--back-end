from config import mydb
import pymysql
conn = mydb.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)
#execute the sql query and commit the connection
def execute(sqlQuery,bindData):
    data = cursor.execute(sqlQuery, bindData)
    return data
    
#commit the connection
def commitConnection():
    conn.commit()

#close the connection   
def closeConnection():
    cursor.close()
    
