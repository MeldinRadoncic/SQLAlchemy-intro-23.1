"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

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
    first_name = db.Column(db.Text,
        nullable=False)
    last_name = db.Column(db.Text,
        nullable=False)
    image_url = db.Column(db.String(250),
        nullable=False,
        default=DEFAULT_IMAGE_URL)


# Post Model
class Post(db.Model):
   

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<Post id = {p.id}, {p.title}, {p.content}, {p.created_at}, {p.user_id}>"

    id = db.Column(db.Integer,
        primary_key=True)
    title = db.Column(db.Text,
         nullable=False)
    content = db.Column(db.Text,
         nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)

    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    # Relationship between User and Post models
    user_post = db.relationship("User", backref="posts")

    # Return Date Time
    @property
    def friendly_date(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

















