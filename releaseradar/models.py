import flask
import flask_login
import itsdangerous

import releaseradar


@releaseradar.login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


subscriptions = releaseradar.db.Table(
    'subscriptions',
    releaseradar.db.Column(
        'user_id', releaseradar.db.Integer,
        releaseradar.db.ForeignKey('user.id'),
        primary_key=True
    ),
    releaseradar.db.Column(
        'artist_id',
        releaseradar.db.Integer,
        releaseradar.db.ForeignKey('artist.id'),
        primary_key=True
    )
)


class User(releaseradar.db.Model, flask_login.UserMixin):
    id = releaseradar.db.Column(releaseradar.db.Integer, primary_key=True)
    username = releaseradar.db.Column(
        releaseradar.db.String(20), unique=True, nullable=False)
    email = releaseradar.db.Column(
        releaseradar.db.String(120), unique=True, nullable=False)
    password = releaseradar.db.Column(
        releaseradar.db.String(60), nullable=False)
    artists = releaseradar.db.relationship(
        'Artist',
        secondary=subscriptions,
        lazy='subquery',
        backref=releaseradar.db.backref('users', lazy=True)
    )

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


class Artist(releaseradar.db.Model):
    id = releaseradar.db.Column(releaseradar.db.Integer, primary_key=True)
    name = releaseradar.db.Column(releaseradar.db.String(100), nullable=False)
    spotify_uri = releaseradar.db.Column(
        releaseradar.db.String(100), unique=True, nullable=False)
    spotify_url = releaseradar.db.Column(
        releaseradar.db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Artist('{self.id}', '{self.spotify_uri}', '{self.name}')"
