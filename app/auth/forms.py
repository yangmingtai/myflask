from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
        TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
        email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                              Email()])
        password = PasswordField('密码', validators=[Required()])
        remember_me = BooleanField('记住我')
        submit = SubmitField('登录')


class RegistrationForm(Form):
        email = StringField('邮箱', validators=[Required(), Length(1, 64),
                            Email()])
        username = StringField('用户名', validators=[
            Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              '用户名只能包含'
                                              '字母、数字、圆点和下划线')])
        password = PasswordField('密码', validators=[
            Required(), EqualTo('password2', message='密码必须一致.')])
        password2 = PasswordField('再次输入密码', validators=[Required()])
        submit = SubmitField('注册')

        def validate_email(self, field):
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('邮箱已被注册.')

        def validate_username(self, field):
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('用户名已被使用.')


class EditProfileForm(Form):
    location = StringField('我的城市或任何地区', validators=[Length(0, 64)])
    constellation = StringField('我的星座', validators=[Length(0, 64)])
    job = StringField('我的身份或工作',  validators=[Length(0, 64)])
    about_me = TextAreaField('我的一句话')
    submit = SubmitField('提交')
