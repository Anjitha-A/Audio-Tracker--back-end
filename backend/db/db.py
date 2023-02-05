from socket import fromshare
import mysql.connector
from app import app
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="new_db"
)
# create table for storing the category lists of audios
mydb_Create_Table_Query = """CREATE TABLE category
(
    categoryid int(100) not null auto_increment,
    category varchar(50) not null,
    CONSTRAINT category_pk PRIMARY KEY (categoryid)
)"""
# # create a table for storing the audio details in the database
mydb_Create_Table_Query = """CREATE TABLE audio
(
  trackid int(100) not null auto_increment PRIMARY KEY,
  title varchar(50) not null,
  artist varchar(50) not null,
  category int(100) not null,
  album varchar(50) not null,
  image varchar(250) not null,
  FOREIGN KEY (category) REFERENCES category(categoryid)
)"""
# # # create role table which specifies the role id and role of user
mydb_Create_Table_Query = """CREATE TABLE role
(
    roleid int(100) not null auto_increment,
    role varchar(50) not null,
    CONSTRAINT role_pk PRIMARY KEY (roleid)
 )"""
# # create a table for storing the details of users
mydb_Create_Table_Query = """CREATE TABLE user
(
  userid int(100) not null auto_increment PRIMARY KEY,
  fullname varchar(50) not null,
  username varchar(50) not null,
  password varchar(250) not null,
  usertype int(100) not null,
  FOREIGN KEY (usertype) REFERENCES role(roleid)
 )"""
# # # create table for add ratings
mydb_Create_Table_Query = """CREATE TABLE rating
(
   rateid int(100) not null auto_increment,
    userid int(100) not null,
    trackid int(100) not null,
    rating int(100) not null,
    FOREIGN KEY (userid) REFERENCES user(userid),
    FOREIGN KEY (trackid) REFERENCES audio(trackid)
)"""
#  create cursor
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print(" Table created successfully ")