from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from . import db, allowed_file, allowed_size
from .models import User, Post, Comments, Likes, Sell
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

    #total likes for each post, total dislikes for each post stored in post.likes or post.dislikes

    #if logged in user has liked post or not

    lip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, liked=True).all()]
    dip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, disliked=True).all()]
    print("Liked Post IDs:", lip)
    for post in posts:
        print("Post ID:", post.pid, "Liked:", post.pid in lip)

    return render_template('browse.html', user=current_user, posts=posts, bounty_posts=bounty_posts, weapons_posts=weapons_posts, advice_posts=advice_posts,  lip=lip, dip=dip)

@routes.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    user_id = current_user.uid  # Assuming user_id is always present in session
    post = Post.query.get_or_404(post_id)

    like_record = Likes.query.filter_by(uid=user_id, pid=post_id).first()

    if like_record:
        if not like_record.liked:
            like_record.liked = True
            like_record.disliked = False  # Ensure a post cannot be both liked and disliked
            post.likes += 1  # Increment likes
            if post.dislikes > 0:
                post.dislikes -= 1  # Decrement dislikes if previously disliked
        else:
            like_record.liked = False  # Toggle like off if already liked
            post.likes -= 1  # Decrement likes
    else:
        like_record = Likes(uid=user_id, pid=post_id, liked=True)
        db.session.add(like_record)
        post.likes += 1  # Increment likes

    db.session.commit()
    return jsonify(success=True)


@routes.route('/dislike_post/<int:post_id>', methods=['POST'])
def dislike_post(post_id):
    user_id = current_user.uid  # Assuming user_id is always present in session
    post = Post.query.get_or_404(post_id)

    like_record = Likes.query.filter_by(uid=user_id, pid=post_id).first()

    if like_record:
        if not like_record.disliked:
            like_record.disliked = True
            like_record.liked = False  # Ensure a post cannot be both liked and disliked
            post.dislikes += 1  # Increment dislikes
            if post.likes > 0:
                post.likes -= 1  # Decrement likes if previously liked
        else:
            like_record.disliked = False  # Toggle dislike off if already disliked
            post.dislikes -= 1  # Decrement dislikes
    else:
        like_record = Likes(uid=user_id, pid=post_id, disliked=True)
        db.session.add(like_record)
        post.dislikes += 1  # Increment dislikes

    db.session.commit()
    return jsonify(success=True)

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

@routes.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # Check if the current user is the author of the post
    if post.uid != current_user.uid:
        print("lol")  # Forbidden - user is not authorized to delete this post

    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('routes.profile'))

@routes.route('/profile')
def profile():
    num_posts = Post.query.filter_by(uid=current_user.get_id()).count()
    total_likes = Post.query.filter_by(uid=current_user.get_id()).with_entities(func.sum(Post.likes)).scalar()
    total_likes = total_likes if total_likes else 0  # Handle case where total_likes is None
    print(total_likes, num_posts)
    purchased_items = Sell.query.filter_by(uid=current_user.get_id(), sold=current_user.get_id()).all()
    current_user_posts = Post.query.filter_by(uid=current_user.get_id()).all()


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
            print(save_path)
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

@routes.route('/marketplace')
def marketplace():
    all_posts = Sell.query.filter_by(sold="Unsold").all()
    return render_template("marketplace.html", user=current_user, posts=all_posts)

@routes.route('/sell', methods =['GET', 'POST'])
def sell():
    if request.method == 'POST':
        weapon_image = request.files.get('weapon_image') #parameter is the name
        weapon_title = request.form.get('weapon_title') #parameter is the name
        weapon_price = request.form.get('weapon_price')
        weapon_desc = request.form.get('weapon_description')
        if weapon_image and allowed_file(weapon_image.filename) and allowed_size(weapon_image): 
            filename = secure_filename(weapon_image.filename)
            save_path = os.path.join(r'app\static\images\sellpics', filename)
            new__item_listing = Sell(uid=current_user.get_id(), price=weapon_price, title=weapon_title, img=filename, desc=weapon_desc)
            db.session.add(new__item_listing)
            db.session.commit()
            flash('Successfully Listed Item!', category='success')
            print(save_path)
            weapon_image.save(save_path)
        if not weapon_title or not weapon_price or not weapon_desc:
            flash("Please fill in all fields", category='error')
        if not allowed_file(weapon_image.filename) or not allowed_size(weapon_image):
            flash("Invalid file format or file is too big, must be below 10mb and png/jpg/jpeg", category='error')
        # if not weapon_title or weapon_price:
        #     flash("Please fill in all fields", category='error')
    return render_template("sell.html", user=current_user)

@routes.route('/purchase/<int:sid>')
def purchase(sid):
    post_wanted = Sell.query.filter_by(sid=sid).first()
    print(post_wanted)
    # Logic for purchasing the item with post_id
    # You can retrieve the post details using the post_id and perform any necessary actions, such as updating the database
    
    # After processing the purchase, you can redirect the user to a confirmation page or any other appropriate page
    return render_template("purchase.html", post_wanted = post_wanted, user=current_user)

@routes.route('/purchase_confirmation/<int:sid>', methods=['POST'])
def purchase_confirmation(sid):
    sold = Sell.query.filter_by(sid=sid, sold="Unsold").first()  # Find the entry with the given sid

    if sold:
        sold.sold = current_user.get_id()  # Delete the entry from the session
        db.session.commit()  # Commit the transaction
        flash('Purchase Completed :)', category='success')

    else:
        flash('Entry not found', category='error')
    # Render the purchase confirmation page
    return redirect(url_for('routes.marketplace'))