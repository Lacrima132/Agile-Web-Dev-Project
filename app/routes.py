from app import app
from flask import render_template, url_for

@app.route('/')
@app.route('/home')
@app.route('/user/<name>')
def user():
    name = 'User'
    return render_template('index.html', name=name)