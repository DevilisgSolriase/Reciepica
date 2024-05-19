import secrets
import os
from PIL import Image
from __init__ import app, db, bcrypt
from flask import Flask, render_template, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm, UpdateAccountForm, NewPostForm, Search, UpdateAccountBio
from models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from random import sample

@app.route("/home", methods=['GET', 'POST'])
def home():
    search = Search()
    result_ids = request.args.getlist('result_ids', type=int)
    results = Post.query.filter(Post.id.in_(result_ids)).all() if result_ids else None
    all_posts = Post.query.all()
    all_users = User.query.order_by(User.id).all()
    sample_size = min(len(all_users), 8)
    random_users = sample(all_users, sample_size)
    return render_template('main_page.html', posts = all_posts, users = random_users, search=search, results=results)

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login unsuccessful, Please try again.', 'fail')
    return render_template('login.html', form = form)

@app.route("/Logout")
def Logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/Register", methods=['GET', 'POST'])
def Reg():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!', 'success')
        return redirect(url_for('Login'))
    return render_template('registration.html', form=form)

@app.route("/Profile", methods=['GET', 'POST'])
def Prof():
    search = Search()
    return render_template('profile.html')

def save_img(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    img_fn = random_hex+f_ext
    img_path = os.path.join(app.root_path, 'static/imgs', img_fn)
    
    output_size = (125, 125)
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(img_path)
    
    return img_fn

@app.context_processor
def base():
    search = Search()
    return dict(search = search)   

@app.route("/search", methods=['POST'])
@login_required
def search():
    search = Search()
    if search.validate_on_submit():
        search_term = search.title.data
        results = Post.query.filter(Post.title.like('%'+search_term+'%'))
        #results = results.order_by(Post.title).all()
        if results:
            return render_template('search_page.html', results=results)
        else:
            flash('There are no Recipes with that title', 'warning')

@app.route("/Profile personal", methods=['GET', 'POST'])
@login_required
def Prof_per():
    form = UpdateAccountForm()
    bio_update = UpdateAccountBio()
    if form.validate_on_submit():
        if form.img.data:
            img_file = save_img(form.img.data)
            current_user.image_file = img_file
        else:
            current_user.image_file = 'static/imgs/images.png'        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account data has been updated!')
        return redirect(url_for('Prof_per'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    if bio_update.validate_on_submit():
        current_user.bio = bio_update.bio.data
        db.session.commit()
        flash(f'Your account bio has been updated!', 'success')
        return redirect(url_for('Prof_per'))
    elif request.method == 'GET':
        bio_update.bio.data = current_user.bio
    user_posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('profile_personal.html', form = form, posts=user_posts, bio_update=bio_update)

@app.route("/recipe")
def rec():
    return render_template('recipe_page.html')

@app.route("/Forgot password")
def forg():
    return render_template('forgotPassword.html')

@app.route("/Profile persoanl/New post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        if form.image_post.data:
            img_file = save_img(form.image_post.data)
        post = Post(
            image_post= img_file,        
            title = form.title.data,
            content = form.content.data,
            user_id = current_user.id    
        )    
        db.session.add(post)
        db.session.commit()
        flash(f'Post Has been created!', 'success')
        return redirect(url_for('Prof_per'))
    return render_template('New_Post.html', form = form)
