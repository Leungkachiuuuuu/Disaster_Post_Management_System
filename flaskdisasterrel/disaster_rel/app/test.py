from app import app
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from app import db
from flask import request
from werkzeug.urls import url_parse
import pytest

@app.route('/')
@app.route('/index')
@login_required


def pytest_login1(password):
    #we create an User object john in routes.py
    #we want to test it by giving it correct password and false password
    username = "john5"
    correct_password = "pass"
    user = User.query.filter_by(username=username).first()
    if user.check_password(password) == True:
        print("correct password")
    else:
        print("Invalid password")
    assert 0

def pytest_direct(password):
    username = "john5"
    correct_password = "pass"
    user = User.query.filter_by(username=username).first()
    if user.check_password(password) == True:
        next_page = request.args.get('next')
    ## Donot how to implement the login front page to back end to test.
    pass

def pytest_dup_username():
    u = User(username='john5',email="asdf@gmail.com")
    #db.session.add(u) fail
    #db.session.commit()
    pass
