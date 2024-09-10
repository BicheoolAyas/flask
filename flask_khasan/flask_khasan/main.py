import sqlalchemy
from flask import Flask, render_template, request, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# Configure the postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:qwerty@127.0.0.1/news'
app.config['SQLALCHEMY_ECHO'] = True # logs db

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

# Forms
from wtforms import Form, StringField, TextAreaField, SelectField

class PostForm(Form):
    title = StringField('Заголовок статьи')
    content = TextAreaField('Текст статьи', render_kw={'rows': 15})
    category = SelectField('Категория:', choices=[])


@app.route('/')
@app.route('/index')
def index():
    """Главная страница"""
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('news/index.html',
                           title='Главная',
                           categories=categories,
                           posts=posts)

@app.route('/category/<int:id>')
def category_list(id: int):
    """Реакция на нажатие кнопок категорий"""
    categories = Category.query.all()
    posts = Post.query.filter(Post.category_id == id)
    current = Category.query.get(id)
    return render_template('news/index.html',
                           title=current,
                           categories=categories,
                           posts=posts,
                           current=current)

@app.route('/post/<int:id>')
def post_detail(id: int):
    """Статья на отдельной странице"""
    post = Post.query.filter(Post.id == id).first() # более современный вариант
    # post = Post.query.get(id) # более старый вариант
    # post = db.session.get(Post, id) # Или даже так
    # post = db.session.execute(db.select(Post).filter_by(id=id)).scalar()

    return render_template('news/post_detail.html', post=post)

@app.route('/search/', methods=['GET'])
def search_resault():
    """for search"""
    q = request.args.get('q')
    categories = Category.query.all()
    search = Post.title.contains(q) | Post.content.contains(q)
    posts = Post.query.filter(search).all()
    if not posts:
        abort(404)
    return render_template('news/index.html',
                           categories=categories,
                           posts=posts)

@app.errorhandler(404)
def page404(e):
    return render_template('news/404.html'), 404

@app.route('/post/create', methods=['POST', 'GET'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        category_id = Category.query.filter(Category.title == category).first().id

        post = Post(title=title, content=content, category_id=category_id)
        db.session.add(post)
        db.session.commit()

        return redirect(url_for('category_list', id=category_id))

    categories = Category.query.all()
    form = PostForm()
    form.category.choices = [cat.title for cat in categories]
    return render_template('news/create_post.html', form=form)



# Utils

@app.template_filter('time_filter')
def jinja2_filter_datatime(date):
    format = '%d.%m.%Y %H:%M:%S'
    return date.strftime(format)

if __name__ == '__main__':
    app.run(debug=True)