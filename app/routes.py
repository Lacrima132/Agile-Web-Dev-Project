from app import app
from flask import render_template, url_for

@app.route('/')
@app.route('/index')
@app.route('/user/<name>')
def index():
    name = 'User'
    return render_template('index.html', name=name)

@app.route('/browse')
def browse():
    name = 'User'
    return render_template('browse.html', name=name)

@app.route('/faq')
def faq():
    name = 'User'
    return render_template('faq.html', name=name)

@app.route('/login')
def login():
    name = 'User'
    return render_template('login.html', name=name)

@app.route('/ranking')
def ranking():
    name = 'User'
    return render_template('ranking.html', name=name)

@app.route('/submit')
def submit():
    name = 'User'
    return render_template('submit.html', name=name)

