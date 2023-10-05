"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request, flash, session
from models import connect_db, User, Post, db, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = 'shhh'

connect_db(app)


@app.get('/')
def root():
    ''' redirect to list of users '''

    return redirect('/users')


@app.get('/users')
def show_users():
    ''' display a list of Blogly users '''

    users = User.query.order_by(User.first_name)

    return render_template('users.html', users=users)


@app.get('/users/new')
def show_new_user_form():
    ''' show the create new user form '''

    return render_template('new_user.html')


@app.post('/users/new')
def create_new_user():
    ''' takes in new user form data and makes a new user '''

    data = request.form
    image = data["image_url"] or None
    new_user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        image_url=image)

    db.session.add(new_user)
    db.session.commit()

    flash(f'New user {new_user.first_name} {new_user.last_name} created')
    return redirect('/users')


@app.get('/users/<user_id>')
def show_user(user_id):
    ''' show a particular user '''

    user = User.query.get_or_404(user_id)

    return render_template('profile.html', user=user, posts=user.posts) #TODO: jinja already has user.posts access


@app.get('/users/<user_id>/edit')
def edit_user(user_id):
    ''' edit information about a particular user '''

    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)


@app.post('/users/<user_id>/edit')
def update_user(user_id):
    ''' receive edit information about a particular user and update db '''

    data = request.form
    user = User.query.get_or_404(user_id)

    user.first_name = data['first_name'] or user.first_name
    user.last_name = data['last_name'] or user.last_name
    user.image_url = data['image_url'] or DEFAULT_IMAGE_URL

    db.session.commit()

    flash(f'Succesfully updated user {user.first_name} {user.last_name}')
    return redirect(f'/users')


@app.post('/users/<user_id>/delete')
def delete_user(user_id):
    ''' deletes a particular user from the database '''
    #TODO:after changing fk to not nullable, delete all user's posts before deleting user
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.first_name} {user.last_name} successfully deleted')
    return redirect('/users')


# User's Posts section

@app.get('/posts/<post_id>')
def show_post(post_id):
    ''' show a specific post '''

    post = Post.query.get_or_404(post_id)
    author = post.user.first_name + ' ' + post.user.last_name #TODO: do in jinja

    return render_template(f'post.html', post=post, author=author) #TODO: #use backref to get author


# New Posts

@app.get('/users/<user_id>/posts/new')
def show_new_post_form(user_id):
    ''' show the new post form '''

    user = User.query.get_or_404(user_id)

    return render_template('new_post.html', user=user)


@app.post('/users/<user_id>/posts/new')
def create_new_post(user_id):
    ''' take information from new post form and add a post to the db '''

    data = request.form

    post = Post(
        title=data["post_title"] or None,
        content=data["post_content"] or 'No Post Content',
        user_id=user_id)

    db.session.add(post)
    db.session.commit()

    flash('Created a new post')

    return redirect(f'/users/{user_id}')


# Edit Posts

@app.get('/posts/<post_id>/edit')
def show_edit_post_form(post_id):
    ''' show the new post form '''

    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)


@app.post('/posts/<post_id>/edit')
def edit_post(post_id):
    ''' take user information from edit post form and add a post to the db '''

    data = request.form
    post = Post.query.get_or_404(post_id)

    post.title = data['post_title']
    post.content = data['post_content']
    db.session.commit()

    flash(f'{post.title} Edited')

    return redirect(f'/posts/{post_id}')


# Delete Post

@app.post('/posts/<post_id>/delete')
def delete_post(post_id):
    '''delete a post from the db '''

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id

    db.session.delete(post)
    db.session.commit()

    flash('Post Deleted')

    return redirect(f'/users/{user_id}')
