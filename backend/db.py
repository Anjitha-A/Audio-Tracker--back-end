import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "audiodatabase"
)
#create a table for storing the audio details in the database
mydb_Create_Table_Query = """CREATE TABLE audio
( 
  trackid int(100) not null auto_increment,
  title varchar(50) not null,
  category varchar(50) not null,
  author  varchar(50) not null,
  image varchar(250) not null,
  rating int(20),
  CONSTRAINT audio_pk PRIMARY KEY (trackid)
)"""
# create a table for storing the details of users 
mydb_Create_Table_Query = """CREATE TABLE user
(
  userid int(100) not null auto_increment,
  fullname varchar(50) not null,
  username varchar(50) not null,
  password varchar(50) not null,
  usertype varchar(50) not null,
  CONSTRAINT user_pk PRIMARY KEY (userid)

   )"""
#create cursor 
cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print(" Table created successfully ")
