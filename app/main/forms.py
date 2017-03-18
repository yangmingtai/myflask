from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PostArticleForm(FlaskForm):
    title = StringField('标题', validators=[Required()])
    body = TextAreaField('内容', validators=[Required()])
    submit = SubmitField('提交')
