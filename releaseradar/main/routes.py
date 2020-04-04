import flask
import flask_login

main = flask.Blueprint('main', __name__)


@main.route("/")
def home():
    if flask_login.current_user.is_authenticated:
        return flask.redirect(flask.url_for('users.artists'))
    return flask.render_template('home.html')
