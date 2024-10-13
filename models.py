from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Users(db.Model):
    """User model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullubale=False, unique=True)
    password = db.Column(db.Text, nullubale=False)
    password = db.Column(db.String(50), nullubale=False, unique=True)
    first_name = db.Column(db.String(30), nullubale=False)
    last_name = db.Column(db.String(30), nullubale=False)