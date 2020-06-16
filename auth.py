from flask import current_app as app
from flask import render_template, request, session, redirect, flash, url_for
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy import or_
from models import db, User
from app import login_manager
from forms import *
import routes

def validate_signup(form):
    username = form.get('username')
    email = form.get('email')
    #existing_user = User.query.filter(or_(email=email, username=username)).first()
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False
    try:
        user = User(username=username, email=email)
        user.set_password(form.get('password'))
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return False
    return user

def validate_login(form):
    username = form.get('username')
    password = form.get('password')
    try:
        user = User.query.filter_by(username=username).first()
    except:
        return False
    if user and user.check_password(password=password):
        return user
    return False

@app.route('/login', methods=['GET', 'POST'])
def login():
   form = LoginForm(request.form)
   if request.method == 'POST' and form.validate_on_submit():
       user = validate_login(request.form)
       if not user:
           message = 'Username/Password not found!'
           return render_template('login.html',
                                   form=LoginForm(None),
                                   message=message)
       login_user(user)
       return redirect(url_for('home'))
   if form.errors:
       message = 'Username/Password not found!'
   else:
       message = 'Login to continue'
   return render_template('login.html', form=LoginForm(None), message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = validate_signup(request.form)
        if not user:
            message = 'User Already Exists!!'
            return render_template('signup.html', message=message, form=SignupForm(None))
        login_user(user)
        return redirect(url_for('home'))
    if form.errors:
        message = 'Please check errors'
    else:
        message = 'Welcome! Signup to begin!'
    return render_template('signup.html', form=form, username_error=form.username.errors,
                            password_error=form.password.errors,
                            confirm_error=form.confirm.errors,
                            email_error=form.email.errors,
                            message=message)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))
