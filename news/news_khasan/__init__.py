from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# Configure the postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:qwerty@127.0.0.1/news'
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_ECHO'] = True # logs db

# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)
