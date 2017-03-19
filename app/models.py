from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from markdown import markdown
import bleach


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(128))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Article %r>' % self.name

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'h4', 'p', 'br']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(
                value, out_format='html'), tags=allowed_tags, strip=True))


db.event.listen(Article.body, 'set', Article.on_changed_body)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # 星座
    constellation = db.Column(db.String(12), default='未知')
    # 加入日期
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 职业
    job = db.Column(db.String(64), default='未知')
    # 简介
    introduce = db.Column(db.String(256), default='')
    # 管理员权限
    admin = db.Column(db.Boolean, default=False)
    # 坐标/地区
    location = db.Column(db.String(64), default='未知')
    articles = db.relationship('Article', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
