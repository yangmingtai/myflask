from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


class PostArticleForm(FlaskForm):
    title = StringField('标题', validators=[Required()])
    body = PageDownField('内容(换行等于两个空格加回车，其他快捷语法请参照markdown语法)', validators=[Required()])
    submit = SubmitField('提交')
