"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


# MODELS

class User(db.Model):
    """ USER """

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id = {u.id}, {u.first_name}, {u.last_name}, {u.image_url}>"

    id = db.Column(db.Integer,
        primary_key=True,
        autoincrement = True)
    first_name = db.Column(db.String(100),
        nullable=False)
    last_name = db.Column(db.String(100),
        nullable=False,
        unique=True)
    image_url = db.Column(db.String(90),
        nullable = True,
        unique = True)
