# create a class Category which have the details of categories of songs
class Category:
    def __init__(self, categoryid: str, category: str):
        self.categoryid = categoryid
        self.category = category
# creating a class Audio which have all the audio details
class Audio:
    def __init__(self, trackid: str, title: str, artist: str, category: int, album: str, image: str):
        self.trackid = trackid
        self.title = title
        self.artist = artist
        self.category = category
        self.album = album
        self.image = image
# create role class
class Role:
    def __init__(self, roleid: str, role: str):
        self.roleid = roleid
        self.role = role
#create user class
class User:
    def __init__(self, userid:str, fullname:str, username:str, password:str, usertype: str):
        self.userid = userid
        self.fullname = fullname
        self.username = username
        self.password = password
        self.usertype = usertype
# create class for ratings
class Rating :
    def __init__(self, rateid:str, userid:str, trackid:str, rating:str):
        self.rateid = rateid
        self.userid = userid
        self.trackid = trackid
        self.rating = rating

        
