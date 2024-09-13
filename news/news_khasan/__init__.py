from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# create the app
app = Flask(__name__)

# Configure the postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:qwerty@127.0.0.1/news'
UPLOAD_FOLDER = 'news_khasan/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = ['Very Secret Key']
# app.config['SQLALCHEMY_ECHO'] = True # logs db

# create the extension
db = SQLAlchemy()

# initialize the app with the extension
db.init_app(app)
migrate = Migrate(app, db)
