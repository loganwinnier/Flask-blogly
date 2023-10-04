"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User table model for database contains id,
    first_name, last_name, image_url
    """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,  # can you use serial to get auto increment
        primary_key=True,
        autoincrement=True)

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
        default="https://miro.medium.com/v2/resize:fit:479/0*5bRx6RbvKwCG5ig5.jpg"
    )
