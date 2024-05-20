from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from . import db, allowed_file, allowed_size
from .models import User, Post, Comments, Likes, Sell, Promote
from .forms import SearchForm, CommentForm, DiscussionForm, ProfileEditForm, SellForm, BountyForm
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
    posts = Post.query.filter_by(claimed=False).all()
    not_sold = Sell.query.filter_by(sold="Unsold").all()
    posts += not_sold  # Combine posts and not_sold

    if form.validate_on_submit():
        keyword = form.keyword.data.strip()
        if keyword:  # If keyword is not empty
            keywords = keyword.split()  # Split the keyword into individual words
            filtered_posts = []

            for post in posts:
                for kw in keywords:
                    if kw.lower() in post.title.lower():  # or kw.lower() in post.desc.lower():
                        filtered_posts.append(post)
                        break

            posts = filtered_posts
            if not filtered_posts:
                flash("No posts match your search", category='error')
        else:
            posts = Post.query.filter_by(claimed=False).all() + Sell.query.filter_by(sold="Unsold").all()  # Reset to all posts

    bounty_posts = Post.query.filter(Post.flag == "Bounty").all()
    advice_posts = Post.query.filter(Post.flag == "Discussion").all()
    weapons_posts = Sell.query.filter().all()

    lip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, liked=True).all()]
    dip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, disliked=True).all()]

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


    lip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, liked=True).all()]
    dip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, disliked=True).all()]

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

    return render_template('post.html', user=current_user, post=post, comments=comments, form=form, lip=lip, dip=dip)
@routes.route('/view-other-userpf/<int:user_id>', methods=['GET', 'POST'])
def view_userpf(user_id):
    userinfo = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(uid=user_id, claimed=False).all()
    not_sold = Sell.query.filter_by(uid=user_id, sold="Unsold").all()
    posts += not_sold  # Combine posts and not_sold

    # Generate these lists based on the currently logged in user
    lip = [like.pid for like in Likes.query.filter_by(uid=current_user.get_id(), liked=True).all()]
    dip = [like.pid for like in Likes.query.filter_by(uid=current_user.get_id(), disliked=True).all()]

    promoted_by_current_user = Promote.query.filter_by(promoted_by=current_user.get_id(), promoted=True, promoting_this_guy=user_id).first()

    return render_template('view-other-userpf.html', user=current_user, userinfo=userinfo, posts=posts, promoted_by_current_user=promoted_by_current_user, lip=lip, dip=dip)



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
    if hunter.promote > 0:
        hunter.rank = "D"
    elif hunter.promote > 10:
        hunter.rank = "C"
    elif hunter.promote > 20:
        hunter.rank = "B"
    elif hunter.promote > 30:
        hunter.rank = "A"
    elif hunter.promote > 40:
        hunter.rank = "S"
    elif hunter.promote > 50:
        hunter.rank = "SS"
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
                img=filename
            )
            db.session.add(new_disc_post)
            db.session.commit()
            flash('Discussion Post Uploaded!', category='success')
            return redirect(url_for('routes.discussion'))
        else:
            flash("Invalid file format. PNG, JPG, JPEG accepted", category='error')

    return render_template('discussion.html', user=current_user, form=form)

@routes.route('/post/delete/<int:post_id>/<string:post_flag>', methods=['POST'])
@login_required
def delete_post(post_id, post_flag):
    if post_flag == "Discussion" or post_flag == "Bounty":
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'success')
    elif post_flag == "Listing":
        post = Sell.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        flash('Listing deleted successfully', 'success')
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
    num_posts = Post.query.filter_by(uid=current_user.get_id(), claimed=False).count() + Sell.query.filter_by(uid=current_user.get_id(), sold="Unsold").count()
    total_likes = Post.query.filter_by(uid=current_user.get_id()).with_entities(func.sum(Post.likes)).scalar()
    total_likes = total_likes if total_likes else 0  # Handle case where total_likes is None
    purchased_items = Sell.query.filter_by(sold=current_user.get_id()).all()
    current_user_posts = Post.query.filter_by(uid=current_user.get_id()).all()
    sold_items = Sell.query.filter_by(uid=current_user.get_id(), sold="Unsold").all()
    disc_posts = Post.query.filter_by(uid=current_user.get_id(), flag="Discussion").all()
    bounties_claimed = Post.query.filter_by(claimed=current_user.get_id()).all()
    bounties_listed = Post.query.filter_by(uid=current_user.get_id(), flag="Bounty", claimed=False).all()
    
    sold_items = sold_items + bounties_listed
    return render_template('profile.html', user=user, num_posts=num_posts, total_likes=total_likes, current_user_posts=current_user_posts, purchased_items=purchased_items, sold_items=sold_items, disc_posts=disc_posts, bounties_claimed=bounties_claimed, bounties_listed=bounties_listed)

@routes.route('/editprofile', methods=['GET', 'POST'])
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
            if previous_avatar_filename != "pfp.png":
                previous_avatar_path = os.path.join('app', 'static', 'images', 'profilepics', previous_avatar_filename)
                if os.path.exists(previous_avatar_path):
                    os.remove(previous_avatar_path)
        
        if bio:
            current_user.bio = bio
            flash('Bio updated!', category='success')

        if username and username != current_user.username:
            if User.query.filter_by(username=username).first():
                flash('Username already in use.', category='error')
            else:
                current_user.username = username
                flash('Username updated!', category='success')

        db.session.commit()
        return redirect(url_for('routes.profile'))

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
            new_item_listing = Sell(uid=current_user.get_id(), price=weapon_price, title=weapon_title, img=filename, desc=weapon_desc, flag="Listing")
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
        sold.sold = current_user.get_id()  # Delete the entry from the session, purchased by current user
        db.session.commit()  # Commit the transaction
        flash('Purchase Completed :)', category='success')

    else:
        flash('Entry not found', category='error')
    # Render the purchase confirmation page
    return redirect(url_for('routes.marketplace'))

@routes.route('/bounties')
def bounties():
    bounty_list = Post.query.filter_by(flag="Bounty", claimed=False).all()
    lip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, liked=True).all()]
    dip = [like.pid for like in Likes.query.filter_by(uid=current_user.uid, disliked=True).all()]
    return render_template('bounties.html', user=current_user, bounty_list=bounty_list, lip=lip, dip=dip)

@routes.route('/addbounty', methods=['GET', 'POST'])
def addbounty():
    form = BountyForm()
    if form.validate_on_submit():
        bounty_image = form.weapon_image.data
        target = form.target.data
        price = int(form.price.data)  # Convert to integer
        target_info = form.tinfo.data
        target_status = form.category_menu.data

        if allowed_size(bounty_image):
            filename = secure_filename(bounty_image.filename)
            save_path = os.path.join('app', 'static', 'images', 'posts', filename)
            list_bounty = Post(uid=current_user.get_id(), price=price, title=target, img=filename, desc=target_info, status=target_status, flag="Bounty")
            db.session.add(list_bounty)
            db.session.commit()
            flash('Successfully Listed Item!', category='success')
            bounty_image.save(save_path)
            return redirect(url_for('routes.addbounty'))

        flash("Invalid file format or file is too big, must be below 10mb and png/jpg/jpeg", category='error')
    elif request.method == 'POST':
        flash('Please fill in all fields correctly.', category='error')

    return render_template('add-bounty.html', user=current_user, form=form)

@routes.route ('activate-bounty/<int:bounty_id>', methods=['GET', 'POST'])
def activate_bounty(bounty_id):
    bounty = Post.query.filter_by(pid=bounty_id).first()
    bounty.claimed = False
    bounty.claimed=current_user.get_id()
    db.session.commit()
    flash("Bounty Saved to Profile", category='success')
    return render_template('bounties.html', user=current_user)