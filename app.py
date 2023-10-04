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
    breakpoint()
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
def edit_user():
    ''' edit information about a particular user '''

    return render_template('edit_user.html')


@app.post('/users/<user_id>/edit')
def update_user():
    ''' receive edit information about a particular user and update db '''

    # update db

    return redirect('/users')


@app.post('/users/<user_id>/delete')
def delete_user():
    ''' deletes a particular user and updates db '''

    # update db

    return redirect('/users')
