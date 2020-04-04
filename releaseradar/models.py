import itsdangerous
import flask
from releaseradar import db, login_manager
import flask_login


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


subscriptions = db.Table(
    'subscriptions',
    db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column(
        'artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True)
)


class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    artists = db.relationship('Artist',
                              secondary=subscriptions,
                              lazy='subquery',
                              backref=db.backref('users', lazy=True))

    def get_reset_token(self, expires_sec=1800):
        s = itsdangerous.TimedJSONWebSignatureSerializer(
            flask.current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = itsdangerous.TimedJSONWebSignatureSerializer(
            flask.current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:  # noqa: E722
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    spotify_uri = db.Column(db.String(100), unique=True, nullable=False)
    spotify_url = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Artist('{self.id}', '{self.spotify_uri}', '{self.name}')"
