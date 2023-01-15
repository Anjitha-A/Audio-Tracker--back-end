import mysql.connector

mydb = mysql.connector.connect(

    host = "localhost",

    user = "root",

    password = "password",

    database = "audiodatabase"

)
mydb_Create_Table_Query = """CREATE TABLE audio
( 
  track_id int(100) not null auto_increment,
  title varchar(50) not null,
  category varchar(50) not null,
  author  varchar(50) not null,
  image varchar(250) not null,
  rating int(20),
  CONSTRAINT audio_pk PRIMARY KEY (track_id)
)"""



mydb_Create_Table_Query= """CREATE TABLE user
(email varchar(50) not null,
  username varchar(50) not null,
  password varchar(50) not null,
  usertype varchar(50) not null
  
   )"""





cursor = mydb.cursor()

result = cursor.execute(mydb_Create_Table_Query)

print(" Table created successfully ")
