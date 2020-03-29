import flask
import flask_sqlalchemy
import flask_bcrypt
import flask_login
import flask_mail
from releaseradar import config


db = flask_sqlalchemy.SQLAlchemy()
bcrypt = flask_bcrypt.Bcrypt()
login_manager = flask_login.LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = flask_mail.Mail()


def create_app(config_class=config.Config):
    app = flask.Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from releaseradar.users.routes import users
    from releaseradar.main.routes import main
    from releaseradar.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app


from releaseradar.models import User, Artist, subscriptions  # noqa: F401
