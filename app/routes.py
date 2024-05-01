# from app import app
from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from . import db

routes = Blueprint('routes', __name__)
@routes.route('/')
@routes.route('/home')
@routes.route('/user/<name>')
def home():
    return render_template('home.html', user=current_user)

@routes.route('/browse')
def browse():
    return render_template('browse.html', user=current_user)

@routes.route('/faq')
def faq():
    return render_template('faq.html', user=current_user)

@routes.route('/ranking')
def ranking():
    return render_template('ranking.html', user=current_user)

@routes.route('/submit')
def submit():
    return render_template('submit.html', user=current_user)


@routes.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)

@routes.route('/editprofile')
def editprofile():
    return render_template('edit-profile.html', user=current_user)

@routes.route('/aboutus')
def aboutus():
    return render_template('about-us.html')