"""Blogly application."""

import os

from flask import Flask, redirect, render_template, request
from models import connect_db, User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def root():
    ''' redirect to list of users '''

    return redirect('/users')


@app.get('/users')
def show_users():
    ''' display a list of Blogly users '''

    users = User.query.all()

    return render_template('users.html', users=users)


@app.get('/users/new')
def show_new_user_form():
    ''' show the create new user form '''

    return render_template('new_user.html')


@app.post('/users/new')
def create_new_user():
    ''' takes in new user form data and makes a new user '''
    data = request.form
    new_user = User(first_name=data["first-name"],
                    last_name=data["last-name"],
                    image_url=data["img_url"])

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<user_id>')
def show_user(user_id):
    ''' show a particular user '''
    user = User.query.get(user_id)
    return render_template('profile.html', user=user)


@app.get('/users/<user_id>/edit')
def edit_user(user_id):
    ''' edit information about a particular user '''

    user = User.query.get(user_id)

    return render_template('edit_user.html', user=user)


@app.post('/users/<user_id>/edit')
def update_user(user_id):
    ''' receive edit information about a particular user and update db '''

    data = request.form
    user = User.query.get(user_id)

    user.first_name = data['first_name'] or user.first_name
    user.last_name = data['last_name'] or user.last_name
    user.image_url = data['image_url'] or user.image_url

    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.post('/users/<user_id>/delete')
def delete_user(user_id):
    ''' deletes a particular user from the database '''

    user = User.query.get(user_id)
    db.session.delete(user)

    # why does this not work? v
    # User.query.filter(int(user_id)).delete()

    db.session.commit()

    return redirect('/users')
