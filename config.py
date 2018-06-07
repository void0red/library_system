from flask import Flask
from os import urandom
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={'*': {'origins': 'http://localhost:63343'}}, supports_credentials=True)

app.config['SECRET_KEY'] = urandom(6)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
