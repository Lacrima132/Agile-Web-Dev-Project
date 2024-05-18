from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from .forms import SignUpForm, LoginForm, ChangePasswordForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('routes.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password1 = form.password1.data
        is_bounty_hunter = form.is_bounty_hunter.data == 'yes'
    
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in use.', category='error')
        elif len(username) < 6:
            flash('Username must be longer than 5 characters.', category='error')
        elif len(password1) < 7:
            flash('Invalid password: must be at least 7 characters.', category='error')
        else:
            password_hash = generate_password_hash(password1, method='pbkdf2:sha256')
            new_user = User(email=email, username=username, password=password_hash, avatar='profile.png', isHunter=is_bounty_hunter)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('routes.home'))
    else:
        if request.method == 'POST':
            flash("Please fill out all fields correctly", category='error')

    return render_template("signup.html", user=current_user, form=form)

@auth.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.old_password.data):
            hashed_password = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
            current_user.password = hashed_password
            db.session.commit()
            flash('Password changed successfully!', category='success')
            return redirect(url_for('routes.profile'))
        else:
            flash('Invalid old password. Please try again.', category='error')
    return render_template('change-password.html', user=current_user, form=form)