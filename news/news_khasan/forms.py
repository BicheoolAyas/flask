from wtforms import Form, StringField, TextAreaField, SelectField, FileField


class PostForm(Form):
    title = StringField('Заголовок статьи')
    content = TextAreaField('Текст статьи', render_kw={'rows': 15})
    category = SelectField('Категория:', choices=[])
    picture = FileField('Картинка для статьи')
