from app import app
from services.admin.audio import *
from services.admin.role import *
from services.admin.category import *
from services.auth import *
from services.user.rating import *
from services.user.search import *
from services.logger import *

if __name__ == "__main__":  
    app.run(debug = True)