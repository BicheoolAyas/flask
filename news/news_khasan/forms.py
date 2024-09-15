from wtforms import Form, StringField, TextAreaField, SelectField, FileField
from wtforms import PasswordField, validators

class PostForm(Form):
    title = StringField('Заголовок статьи')
    content = TextAreaField('Текст статьи', render_kw={'rows': 15})
    category = SelectField('Категория:', choices=[])
    picture = FileField('Картинка для статьи')


class Registration(Form):
    """Форма для регистрации пользователя"""
    username = StringField('login*', [validators.DataRequired()])
    first_name = StringField('Name*', [validators.DataRequired()])
    last_name = StringField('Lastname*', [validators.DataRequired()])
    phone = StringField('Phone number')
    email = StringField('Email*', [validators.DataRequired()])
    password = PasswordField('Password', [validators.Length(min=3, max=8),
                                          validators.EqualTo('confirm',
                                                             message='Passwords must match')])
    confirm = PasswordField('Confirm Password*', [validators.DataRequired()])


class UserLogin(Form):
    """Форма для авторизации пользоваеля"""
    username = StringField('Login')
    password = PasswordField('Password')


class UpdateUserProfile(Form):
    """Форма для редактирования поользовательского профайла"""
    username = StringField('Логин',[validators.DataRequired()])
    first_name = StringField('Имя', [validators.DataRequired()])
    last_name = StringField('Фамилия', [validators.DataRequired()])
    phone = StringField('Контактный номер')
    email = StringField('Почта', [validators.DataRequired()])
    bio = TextAreaField('БИО', render_kw={'rows': 5})
    photo = FileField('Аватарка')