from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from . import db, allowed_file, allowed_size
from .models import User, Post, Comments, Likes, Sell, Promote
from .forms import SearchForm, CommentForm, DiscussionForm, ProfileEditForm, SellForm
from werkzeug.utils import secure_filename
from flask_wtf import CSRFProtect
from sqlalchemy import func
import os


routes = Blueprint('routes', __name__)
@routes.route('/')
@routes.route('/home')
@routes.route('/user/<name>')
def home():
    return render_template('home.html', user=current_user)

@routes.route('/browse', methods=['GET', 'POST'])
def browse():
    form = SearchForm()
    posts = Post.query.all()  # Retrieve all posts initially

    if form.validate_on_submit():
        keyword = form.keyword.data
        keywords = keyword.split()  # Split the keyword into individual words
        filtered_posts = []

        for post in posts:
            for kw in keywords:
                if kw.lower() in post.title.lower():  # or kw.lower() in post.desc.lower():
                    filtered_posts.append(post)
                    break

        posts = filtered_posts
        if len(keyword) == 0:
            posts = Post.query.all()             
        elif len(filtered_posts) == 0:
            flash("No posts match your search", category='error')
    
    bounty_posts = Post.query.filter(Post.flag == "Bounty").all()
    advice_posts = Post.query.filter(Post.flag == "Advice").all()
    weapons_posts = Post.query.filter(Post.flag == "Weapons").all()

    lip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, liked=True).all()]
    dip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, disliked=True).all()]
    print("Liked Post IDs:", lip)
    for post in posts:
        print("Post ID:", post.pid, "Liked:", post.pid in lip)

    return render_template('browse.html', user=current_user, form=form, posts=posts, bounty_posts=bounty_posts, weapons_posts=weapons_posts, advice_posts=advice_posts, lip=lip, dip=dip)

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
    form = CommentForm()

    if form.validate_on_submit():
        comment_text = form.comment.data
        new_comment = Comments(
            pid=post_id,
            uid=current_user.get_id(),
            comment=comment_text,
            timestamp=func.now()
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment Added!', category='success')
        return redirect(url_for('routes.post', post_id=post_id))

    return render_template('post.html', user=current_user, post=post, comments=comments, form=form)
@routes.route('/view-other-userpf/<int:user_id>', methods = ['GET','POST'])
def view_userpf(user_id):
    userinfo = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(uid=user_id).all()
    promoted_by_current_user = Promote.query.filter_by(promoted_by=current_user.get_id(), promoted=True, promoting_this_guy=user_id).first()

    return render_template('view-other-userpf.html', user=current_user, userinfo=userinfo, posts=posts, promoted_by_current_user=promoted_by_current_user)

@routes.route('/promote_user/<int:user_id>', methods=['POST'])
def promote_user(user_id):
    promote_hunter = Promote.query.filter_by(promoted_by=current_user.get_id(), promoting_this_guy=user_id).first()
    hunter = User.query.get_or_404(user_id)
    
    if promote_hunter:
        if not promote_hunter.promoted:
            promote_hunter.promoted = True
            hunter.promote += 1  # Increment promotion count
        else:
            promote_hunter.promoted = False  # Toggle promotion off if already promoted
            hunter.promote -= 1  # Decrement promotion count
    else:
        promote_hunter = Promote(promoted_by=current_user.get_id(), promoting_this_guy=user_id, promoted=True)
        db.session.add(promote_hunter)
        hunter.promote += 1  # Increment promotion count
    db.session.commit()
    return jsonify(success=True, promotion_count=hunter.promote)

@routes.route('/faq')
def faq():
    return render_template('faq.html', user=current_user)

@routes.route('/ranking')
def ranking():
    highest_promoted = User.query.order_by(User.promote.desc()).all()
    print(highest_promoted)
    return render_template('ranking.html', user=current_user, highest_promoted=highest_promoted)

@routes.route('/discussion', methods=['GET', 'POST'])
def discussion():
    form = DiscussionForm()
    if form.validate_on_submit():
        title = form.title.data
        image = form.image.data
        desc = form.desc.data
        user_id = current_user.get_id()

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            save_path = os.path.join('app', 'static', 'images', 'posts', filename)
            image.save(save_path)

            new_disc_post = Post(
                title=title,
                desc=desc,
                flag="Discussion",
                uid=user_id,
                img_filename=filename
            )
            db.session.add(new_disc_post)
            db.session.commit()
            flash('Discussion Post Uploaded!', category='success')
            return redirect(url_for('routes.discussion'))
        else:
            flash("Invalid file format. PNG, JPG, JPEG accepted", category='error')

    return render_template('discussion.html', user=current_user, form=form)

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
    user = current_user
    num_posts = Post.query.filter_by(uid=current_user.get_id()).count()
    total_likes = Post.query.filter_by(uid=current_user.get_id()).with_entities(func.sum(Post.likes)).scalar()
    total_likes = total_likes if total_likes else 0  # Handle case where total_likes is None
    print(total_likes, num_posts)
    purchased_items = Sell.query.filter_by(uid=current_user.get_id(), sold=current_user.get_id()).all()
    current_user_posts = Post.query.filter_by(uid=current_user.get_id()).all()
    sold_items = Sell.query.filter_by(uid=current_user.get_id(), sold="Unsold").all()

    return render_template('profile.html', user=user, num_posts=num_posts, total_likes=total_likes, current_user_posts=current_user_posts, purchased_items=purchased_items, sold_items=sold_items)

@routes.route('/editprofile', methods =['GET', 'POST'])
def editprofile():
    form = ProfileEditForm()
    if form.validate_on_submit():
        previous_avatar_filename = current_user.avatar
        avatar = form.image.data
        username = form.username.data
        bio = form.bio.data
        
        if avatar and allowed_file(avatar.filename) and allowed_size(avatar):
            filename = secure_filename(avatar.filename)
            save_path = os.path.join('app', 'static', 'images', 'profilepics', filename)
            avatar.save(save_path)
            current_user.avatar = filename
            flash('Profile picture uploaded!', category='success')
            if previous_avatar_filename:
                previous_avatar_path = os.path.join('app', 'static', 'images', 'profilepics', previous_avatar_filename)
                if os.path.exists(previous_avatar_path):
                    os.remove(previous_avatar_path)
        
        if bio:
            current_user.bio = bio
            flash('Bio updated!', category='success')
        
        if username:
            current_user.username = username
            flash('Username updated!', category='success')

        db.session.commit()
        return redirect(url_for('routes.editprofile'))

    return render_template('edit-profile.html', user=current_user, form=form)

@routes.route('/aboutus')
def aboutus():
    return render_template('about-us.html', user=current_user)

@routes.route('/marketplace')
def marketplace():
    all_posts = Sell.query.filter_by(sold="Unsold").all()
    return render_template("marketplace.html", user=current_user, posts=all_posts)

@routes.route('/sell', methods=['GET', 'POST'])
def sell():
    form = SellForm()
    if form.validate_on_submit():
        weapon_image = form.weapon_image.data
        weapon_title = form.weapon_title.data
        weapon_price = form.weapon_price.data
        weapon_desc = form.weapon_description.data

        if allowed_size(weapon_image):
            filename = secure_filename(weapon_image.filename)
            save_path = os.path.join('app', 'static', 'images', 'sellpics', filename)
            new_item_listing = Sell(uid=current_user.get_id(), price=weapon_price, title=weapon_title, img=filename, desc=weapon_desc)
            db.session.add(new_item_listing)
            db.session.commit()
            flash('Successfully Listed Item!', category='success')
            weapon_image.save(save_path)
            return redirect(url_for('routes.sell'))

        flash("Invalid file format or file is too big, must be below 10mb and png/jpg/jpeg", category='error')
    elif request.method == 'POST':
        flash('Please fill in all fields correctly.', category='error')

    return render_template("sell.html", user=current_user, form=form)

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

@routes.route('/bounties')
def bounties():
    bounty_list = Post.query.filter_by(flag="Bounty").all()
    return render_template('bounties.html', user=current_user, bounty_list=bounty_list)

@routes.route('/addbounty', methods =['GET', 'POST'])
def addbounty():
    if request.method == 'POST':
        bounty_image = request.files.get('weapon_image') #parameter is the name
        target = request.form.get('target') #parameter is the name
        price = request.form.get('price')
        target_info = request.form.get('tinfo')
        if bounty_image and allowed_file(bounty_image.filename) and allowed_size(bounty_image): 
            filename = secure_filename(bounty_image.filename)
            save_path = os.path.join('app','static','images','sellpics', filename)
            # list_bounty = Post(uid=current_user.get_id(), price=price, title=weapon_title, img=filename, desc=weapon_desc)
            # db.session.add(new__item_listing)
            # db.session.commit()
            flash('Successfully Listed Item!', category='success')
            print(save_path)
            bounty_image.save(save_path)
            return render_template("sell.html", user=current_user)
        # if not weapon_title or not weapon_price or not weapon_desc:
        #     flash("Please fill in all fields", category='error')
        # if not allowed_file(weapon_image.filename) or not allowed_size(weapon_image):
        #     flash("Invalid file format or file is too big, must be below 10mb and png/jpg/jpeg", category='error')
        # # if not weapon_title or weapon_price:
        #     flash("Please fill in all fields", category='error')
    return render_template('add-bounty.html', user=current_user)