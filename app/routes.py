from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from . import db, allowed_file, allowed_size
from .models import User
from werkzeug.utils import secure_filename
import os

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

@routes.route('/editprofile', methods =['GET', 'POST'])
def editprofile():
    if request.method == 'POST':
        previous_avatar_filename = current_user.avatar
        avatar = request.files.get('change-image') #parameter is the name
        username = request.form.get('change-username') #parameter is the name
        bio = request.form.get('bio-change')
        if avatar and allowed_file(avatar.filename) and allowed_size(avatar): 
            filename = secure_filename(avatar.filename)
            save_path = os.path.join(r'app\static\images\profilepics', filename)
            print(save_path)
            current_user.avatar = filename
            db.session.commit()
            flash('Profile picture Uploaded!', category='success')
            avatar.save(save_path)
            if previous_avatar_filename:
                previous_avatar_path = os.path.join(r'app\static\images\profilepics', previous_avatar_filename)
                if os.path.exists(previous_avatar_path):
                    os.remove(previous_avatar_path)
        if bio:
            current_user.bio = bio
            db.session.commit()
            flash('Bio Updated!', category='success')
        if username:
            current_user.username = username
            db.session.commit()
            flash('Username Updated!', category='success')
        elif not allowed_file(avatar.filename) and not allowed_size(avatar):
            flash("Invalid file format or file is too big, must be below 10mb and png/jpg/jpeg", category='error')
            
    return render_template('edit-profile.html', user=current_user)

@routes.route('/aboutus')
def aboutus():
    return render_template('about-us.html', user=current_user)