import sqlalchemy
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# Configure the postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:qwerty@127.0.0.1/news'

# initialize the app with the extension
db.init_app(app)

# Create Model
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

class Category(db.Model):
    """Категории постов"""
    __tablename__  = 'category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    posts = db.relationship('Post', back_populates='category')

    def __repr__(self):
        return self.title

class Post(db.Model):
    """Новостные посты"""
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    category_id = mapped_column(ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    def __repr__(self):
        return self.title





@app.route('/')
@app.route('/index')
def index():
    """Главная страница"""
    return render_template('news/index.html', title='Главная')

if __name__ == '__main__':
    app.run(debug=True)