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
        nullable=False
    )

    # for every Post instance, I want to get the User by saying that Post instance.user
    user = db.relationship('User', backref="posts")
    # backref: for every single User instance


class Tag(db.Model):
    ''' Tag model '''

    __tablename__ = "tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(25),
        nullable=False,
        unique=True
    )
    # express route, can't get other columns from post_tags
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

    # post_tags = db.relationship('PostTag', backref='tags')
    # local route - only useful if more columns in posts_tags that you wanted info from


class PostTag(db.Model):
    ''' PostTag model '''

    __tablename__ = "posts_tags"

    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id'),
        primary_key=True,
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id'),
        primary_key=True,
    )