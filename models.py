"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = "https://miro.medium.com/v2/resize:fit:479/0*5bRx6RbvKwCG5ig5.jpg"

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User table model
    """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)  # dont need

    first_name = db.Column(
        db.String(25),
        nullable=False
    )

    last_name = db.Column(
        db.String(25),
        nullable=False
    )

    image_url = db.Column(
        db.String,
        nullable=False,
        default=DEFAULT_IMAGE_URL,
    )
