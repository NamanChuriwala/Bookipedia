import requests
import os
import json
from flask import current_app as app
from flask import render_template, request, session, redirect, flash, url_for
from flask_login import login_required, logout_user, current_user, login_user
from sqlalchemy import or_
from oauthlib.oauth2 import WebApplicationClient
from dotenv import load_dotenv
from models import db, User, GoogleUser
from app import login_manager
from forms import *
import routes

load_dotenv('project1.env')

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
        "https://accounts.google.com/.well-known/openid-configuration"
                       )
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    try:
        return requests.get(GOOGLE_DISCOVERY_URL).json()
    except:
        return None

def validate_signup(form):
    username = form.get('username')
    email = form.get('email')
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
   print(current_user)
   if current_user.is_authenticated:
       return redirect(url_for('home.html'))
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

@app.route('/google_login', methods=['GET', 'POST'])
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        try:
            google_provider_cfg = get_google_provider_cfg()
            authorization_endpoint = google_provider_cfg["authorization_endpoint"]
            request_uri = client.prepare_request_uri(
                            authorization_endpoint,
                            redirect_uri=request.base_url + "/callback",
                            scope=["openid", "email", "profile"],)
            return redirect(request_uri)
        except Exception as e:
            print(e)
            message = 'Login Failed!'
            return render_template('google_login.html',
                                    form=GoogleLogin(None), message=message)
    message = 'Login using your google account!'
    return render_template('google_login.html',
                            form=GoogleLogin(None),
                            message=message)

@app.route('/google_login/callback')
def callback():
    try:
        code = request.args.get("code")
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = client.prepare_token_request(
                                        token_endpoint,
                                        authorization_response=request.url,
                                        redirect_url=request.base_url,
                                        code=code)
        token_response = requests.post(token_url, headers=headers,
                                       data=body,
                                       auth=(GOOGLE_CLIENT_ID,
                                             GOOGLE_CLIENT_SECRET),)
        client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
    except:
        return "User email not verified by Google", 400
    try:
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            users_email = userinfo_response.json()["email"]
            picture = userinfo_response.json()["picture"]
            users_name = userinfo_response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400

        user = GoogleUser.query.filter_by(userid=unique_id).first()
        if not user:
            user = GoogleUser(userid=unique_id, name=users_name, email=users_email)
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for('home'))
    except:
        return "User not verified by Google.", 400


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
