from flask import Flask
from releaseradar import db
from releaseradar.models import User, Artist, subscriptions  # noqa: F401

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db.init_app(app)

with app.app_context():
    db.create_all()
