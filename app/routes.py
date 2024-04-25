# from app import app
from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from . import db

routes = Blueprint('routes', __name__)
@routes.route('/')
@routes.route('/home')
@routes.route('/user/<name>')
def home():
    name = 'User'
    return render_template('home.html', name=name, user=current_user)

@routes.route('/browse')
def browse():
    name = 'User'
    return render_template('browse.html', name=name, user=current_user)

@routes.route('/faq')
def faq():
    name = 'User'
    return render_template('faq.html', name=name, user=current_user)

@routes.route('/ranking')
def ranking():
    name = 'User'
    return render_template('ranking.html', name=name, user=current_user)

@routes.route('/submit')
def submit():
    name = 'User'
    return render_template('submit.html', name=name, user=current_user)


@routes.route('/profile')
def profile():
    name = 'User'
return render_template('profile.html', name=name, user=current_user)

@app.route('/aboutus')
def aboutus():
    name = 'User'
    return render_template('about-us.html', name=name)