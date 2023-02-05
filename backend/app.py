import bcrypt
from flask import Flask
import bcrypt
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)