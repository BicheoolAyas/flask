import os.path as op
import uuid as uuid
from werkzeug.utils import  secure_filename

from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField

from news_khasan import app, db
from news_khasan.models import  Category, Post, Users

def prefix_name(obj, file_data):
    parts = op.splitext(file_data.filename)
    # return secure_filename('file-%s%s' %parts)
    return secure_filename(f'{uuid.uuid1()}_%s%s' %parts)

class AdminAccess(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_anonymous:
            return current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        return  redirect(url_for('index'))

class PostAdmin(ModelView):
    form_columns = ['title', 'content', 'category', 'picture']
    form_extra_fields = {
        'picture': FileUploadField('picture',
                                   namegen=prefix_name,
                                   base_path='news_khasan/static/images')
    }


admin = Admin(app, template_mode='bootstrap4', index_view=AdminAccess())
admin.add_view(ModelView(Category, db.session))
admin.add_view(PostAdmin(Post, db.session))
# admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Users, db.session))
