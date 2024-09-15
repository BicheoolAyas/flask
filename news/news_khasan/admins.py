from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from news_khasan import app, db
from news_khasan.models import  Category, Post, Users

admin = Admin(app, template_mode='bootstrap4')
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Users, db.session))
