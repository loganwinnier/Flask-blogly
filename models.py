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
    )

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

    # instance property
    # posts = db.relationship('Post', backref='user')


class Post(db.Model):
    ''' Post table model '''

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.String(50),
        nullable=False,
        # Unique=(id),
    )

    content = db.Column(
        db.String,
        nullable=False,
        default='',
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.now(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        #TODO: add nullable=False (and drop tables)
    )

    # for every Post instance, I want to get the User by saying that Post instance.user
    user = db.relationship('User', backref="posts")
    # backref: for every single User instance
