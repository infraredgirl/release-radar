import flask
import flask_login
from releaseradar import db, bcrypt, messages, models
from releaseradar.users import forms, utils

users = flask.Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('main.home'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = models.User(username=form.username.data,
                           email=form.email.data,
                           password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flask.flash(messages.ACCOUNT_CREATED, 'success')
        return flask.redirect(flask.url_for('users.login'))
    return flask.render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('main.home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password, form.password.data):
            flask_login.login_user(user, remember=form.remember.data)
            next_page = flask.request.args.get('next')
            return flask.redirect(next_page) if next_page else flask.redirect(
                flask.url_for('main.home'))
        else:
            flask.flash(messages.LOGIN_FAILED, 'danger')
    return flask.render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@flask_login.login_required
def account():
    form = forms.UpdateAccountForm()
    if form.validate_on_submit():
        flask_login.current_user.username = form.username.data
        flask_login.current_user.email = form.email.data
        db.session.commit()
        flask.flash(messages.ACCOUNT_UPDATED, 'success')
        return flask.redirect(flask.url_for('users.account'))
    elif flask.request.method == 'GET':
        form.username.data = flask_login.current_user.username
        form.email.data = flask_login.current_user.email
        artists = flask_login.current_user.artists
    return flask.render_template('account.html', form=form, artists=artists)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('main.home'))
    form = forms.RequestResetForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        utils.send_reset_email(user)
        msg = messages.RESET_PASSWORD_EMAIL_SENT
        flask.flash(msg, 'info')
        return flask.redirect(flask.url_for('users.login'))
    return flask.render_template('reset_request.html',
                                 title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('main.home'))
    user = models.User.verify_reset_token(token)
    if user is None:
        flask.flash(messages.TOKEN_INVALID, 'warning')
        return flask.redirect(flask.url_for('users.reset_request'))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flask.flash(messages.PASSWORD_UPDATED, 'success')
        return flask.redirect(flask.url_for('users.login'))
    return flask.render_template('reset_token.html',
                                 title='Reset Password',
                                 form=form)
