# from app import app
from flask import Blueprint, render_template, url_for

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
@main_bp.route('/index')
@main_bp.route('/user/<name>')
def index():
    name = 'User'
    return render_template('index.html', name=name)

@main_bp.route('/browse')
def browse():
    name = 'User'
    return render_template('browse.html', name=name)

@main_bp.route('/faq')
def faq():
    name = 'User'
    return render_template('faq.html', name=name)

@main_bp.route('/login')
def login():
    name = 'User'
    return render_template('login.html', name=name)

@main_bp.route('/ranking')
def ranking():
    name = 'User'
    return render_template('ranking.html', name=name)

@main_bp.route('/submit')
def submit():
    name = 'User'
    return render_template('submit.html', name=name)

@main_bp.route('/signup')
def signup():
    name = 'User'
    return render_template('signup.html', name=name)

@main_bp.route('/profile')
def profile():
    name = 'User'
    return render_template('profile.html', name=name)