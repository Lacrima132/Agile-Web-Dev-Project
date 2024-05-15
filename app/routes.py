from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from . import db, allowed_file, allowed_size
from .models import User, Post, Comments
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
    posts = Post.query.all()
    return render_template('browse.html', user=current_user, posts=posts)

@routes.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comments.query.filter_by(pid=post_id).all()

    if request.method == 'POST':                        # Upload comments
        comments = request.form.get('comment')
        if comments:
            new_comment = Comments(pid=post_id, uid=current_user.get_id(), comment=comments)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment Added!', category='success')
            return redirect(url_for('routes.post', post_id=post_id))
        else:
            flash('Comment cannot be empty!', category='error')
            return redirect(url_for('routes.post', post_id=post_id))

    return render_template('post.html', user=current_user, post=post, comments=comments)

@routes.route('/view-other-userpf/<int:user_id>', methods = ['GET','POST'])
def view_userpf(user_id):
    userinfo = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(uid=user_id).all()

    return render_template('view-other-userpf.html', user=current_user, userinfo=userinfo, posts=posts)

@routes.route('/faq')
def faq():
    return render_template('faq.html', user=current_user)

@routes.route('/ranking')
def ranking():
    return render_template('ranking.html', user=current_user)

@routes.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
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

@routes.route('/changepassword')
def changepassword():
    return render_template('change-password.html', user=current_user)

@routes.route('/aboutus')
def aboutus():
    return render_template('about-us.html', user=current_user)