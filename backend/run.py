from app import app
from views.admin.audio import *
from views.admin.role import *
from views.admin.category import *
from views.user.user import *
from views.user.rating import *

if __name__ == "__main__":  
    app.run()
