from app import app
from views.admin.audio import *
from views.admin.role import *
from views.admin.category import *
from views.auth import *
from views.user.rating import *
from views.user.search import *
from services.logger import *

if __name__ == "__main__":  
    app.run(debug = True)
