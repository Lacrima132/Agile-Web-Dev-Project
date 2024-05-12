from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user
from . import db, allowed_file, allowed_size
from .models import User, Post
from werkzeug.utils import secure_filename
from sqlalchemy import or_, func
import os


routes = Blueprint('routes', __name__)
@routes.route('/')
@routes.route('/home')
@routes.route('/user/<name>')
def home():
    return render_template('home.html', user=current_user)

@routes.route('/browse', methods=['GET', 'POST'])
def browse():
    keyword = request.form.get('keyword')
    posts = Post.query.all()  # Retrieve all posts initially
    
    if keyword:
        keywords = keyword.split()  # Split the keyword into individual words
        filtered_posts = []
        
        for post in posts:
            for kw in keywords:
                if kw.lower() in post.title.lower(): #or kw.lower() in post.desc.lower():
                    filtered_posts.append(post)
                    break
        
        posts = filtered_posts
        if len(filtered_posts) == 0:
            flash("No posts match your search", category='error')
    
    bounty_posts = Post.query.filter(Post.flag == "Bounty").all()

    # Retrieve all Advice posts
    advice_posts = Post.query.filter(Post.flag == "Advice").all()

    # Retrieve all Weapons posts
    weapons_posts = Post.query.filter(Post.flag == "Weapons").all()
    
    return render_template('browse.html', user=current_user, posts=posts, bounty_posts=bounty_posts, weapons_posts=weapons_posts, advice_posts=advice_posts, )

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
        flag = request.form.get('category-menu')
        if img and allowed_file(img.filename):
            filename = secure_filename(img.filename)
            save_path = os.path.join('app\static\images\posts', filename)
            img.save(save_path)
            new_image = Post(title=title,desc=desc,uid=user_id,img_filename=filename, img_filepath=save_path, flag=flag)
            db.session.add(new_image)
            db.session.commit()
            flash('Post Uploaded!', category='success')
            return redirect(url_for('routes.browse'))
        else:
            flash("Invalid file format. PNG,JPG,JPEG accepted", category='error')

    return render_template('submit.html', user=current_user)

@routes.route('/profile')
def profile():
    num_posts = Post.query.filter_by(uid=current_user.get_id()).count()
    total_likes = Post.query.filter_by(uid=current_user.get_id()).with_entities(func.sum(Post.likes)).scalar()
    total_likes = total_likes if total_likes else 0  # Handle case where total_likes is None
    print(total_likes, num_posts)

    current_user_posts = Post.query.filter_by(uid=current_user.get_id()).all()

    return render_template('profile.html', user=current_user, num_posts = num_posts, total_likes = total_likes, current_user_posts=current_user_posts)

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