from flask import render_template, abort, redirect, url_for, flash, request
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
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(
        Article.timestamp.desc()).paginate(
            page, per_page=20, error_out=False)
    articles = pagination.items
    return render_template('index.html', form=form, articles=articles,
                           pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    articles = user.articles.order_by(Article.timestamp.desc()).all()
    return render_template('user.html', user=user, articles=articles)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.constellation = form.constellation.data
        current_user.location = form.location.data
        current_user.introduce = form.about_me.data
        current_user.job = form.job.data
        db.session.add(current_user)
        flash('资料已更新.')
        return redirect(url_for('.user', username=current_user.username))
    form.job.data = current_user.job
    form.location.data = current_user.location
    form.about_me.data = current_user.introduce
    form.constellation.data = current_user.constellation
    form.username.data = current_user.username
    return render_template('edit_profile.html', form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    article = Article.query.get_or_404(id)
    if current_user != article.author:
        abort(403)
    form = PostArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.body = form.body.data
        db.session.add(article)
        flash('内容已更新.')
        return redirect(url_for('.article', id=article.id))
    form.body.data = article.body
    form.title.data = article.title
    return render_template('edit_article.html', form=form)


@main.route('/article/<int:id>')
def article(id):
    article = Article.query.get_or_404(id)
    return render_template('article.html', articles=[article])
