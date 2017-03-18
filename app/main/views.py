from flask import render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import User
from . import main
from ..auth.forms import EditProfileForm
from ..models import Article, db
from .forms import PostArticleForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data,
                          body=form.body.data,
                          author=current_user._get_current_object())
        db.session.add(article)
        return redirect(url_for('.index'))
    articles = Article.query.order_by(Article.timestamp.desc()).all()
    return render_template('index.html', form=form, articles=articles)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.constellation = form.constellation.data
        current_user.location = form.location.data
        current_user.introduce = form.about_me.data
        current_user.job = form.job.data
        db.session.add(current_user)
        flash('资料已更新.')
        return redirect(url_for('.user', username=current_user.usernaasae))
    form.job.data = current_user.job
    form.location.data = current_user.location
    form.about_me.data = current_user.introduce
    form.constellation = current_user.constellation
    return render_template('edit_profile.html', form=form)
