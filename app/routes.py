from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from . import db, allowed_file, ALLOWED_EXTENSIONS
import os
from .models import Post
from werkzeug.utils import secure_filename

routes = Blueprint('routes', __name__)
@routes.route('/')
@routes.route('/home')
@routes.route('/user/<name>')
def home():
    return render_template('home.html', user=current_user)

@routes.route('/browse')
def browse():
    posts = Post.query.all()
    return render_template('browse.html', user=current_user, posts=posts)

@routes.route('/faq')
def faq():
    return render_template('faq.html', user=current_user)

@routes.route('/ranking')
def ranking():
    return render_template('ranking.html', user=current_user)

@routes.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        print('hello')
        title = request.form.get('target')
        img = request.files.get('image')
        desc = request.form.get('tinfo')
        user_id = current_user.get_id()

        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            save_path = os.path.join('app\static\images\posts', filename)
            img.save(save_path)

            new_image = Post(title=title,desc=desc,uid=user_id,img_filename=filename, img_filepath=save_path)
            db.session.add(new_image)
            db.session.commit()
            flash('Post Uploaded!', category='success')
            return redirect(url_for('routes.browse'))
        else:
            flash("Invalid file format. PNG,JPG,JPEG accepted", category='error')

    return render_template('submit.html', user=current_user)

@routes.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)

@routes.route('/editprofile')
def editprofile():
    return render_template('edit-profile.html', user=current_user)

@routes.route('/aboutus')
def aboutus():
    return render_template('about-us.html', user=current_user)