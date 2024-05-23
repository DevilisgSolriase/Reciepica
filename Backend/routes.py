import secrets
import os
from PIL import Image
from __init__ import app, db, bcrypt
from flask import Flask, render_template, flash, redirect, url_for, request, abort
from forms import RegistrationForm, LoginForm, UpdateAccountForm, NewPostForm, Search, UpdateAccountBio, DataSend, DataUser, UpdatePostForm, DeletePost
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

@app.route("/user", methods=['GET','POST'])
def send_user():
    form = DataUser()
    if request.method == 'POST':
        form.username = request.form.get('username')
        form.bio = request.form.get('bio')
        form.image_file = request.form.get('image_file')
        user = User.query.filter_by(username=form.username).first()
        posts = Post.query.filter_by(user_id= user.id)
    return render_template('profile.html', form=form, posts=posts)    
    

@app.route("/Profile", methods=['GET', 'POST'])
def Prof():
    search = Search()
    return redirect('/Profile')

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
def search():
    search = Search()
    if search.validate_on_submit():
        search_term = search.title.data
        results = Post.query.filter(Post.title.like('%'+search_term+'%'))
        if results:
            return render_template('search_page.html', results=results)
        else:
            flash('There are no Recipes with that title', 'warning')

@app.route("/post/update/post/<int:post_id>", methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    else:
        form = UpdatePostForm()
        if form.validate_on_submit():
            print("test if the if statment for the img works")
            if form.img.data:
                print("test if the if statment for the img works")
                img_file = save_img(form.img.data)
                post.image_post = img_file
            else:
                post.image_post = 'images.png' 
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Your post has been updated!")
            return redirect(url_for('Prof_per'))
        elif request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        print(form.errors)
        return render_template('recipe_page_edit.html', form=form)

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
            current_user.image_file = 'images.png'        
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
    if request.method == 'POST':
        post_id = request.form.get('post_id')
        if post_id:
            post = Post.query.get_or_404(post_id)
            if post.author == current_user:
                db.session.delete(post)
                db.session.commit()
                flash('The post has been deleted successfully')
            else:
                abort(403)
        return redirect(url_for('Prof_per'))
    user_posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('profile_personal.html', form = form, posts=user_posts, bio_update=bio_update)

@app.route("/post",methods=['GET','POST'])
def data_send():
    form = DataSend()
    if request.method == 'POST':
        form.title = request.form.get('title')
        form.content = request.form.get('content')
        form.image_post = request.form.get('image_post')
        all_posts = Post.query.all()
        sample_size = min(len(all_posts), 5)
        random_posts = sample(all_posts, sample_size)
        profile = Post.query.filter_by(title=form.title, content=form.content, image_post=form.image_post).first()
        if not form.image_post:
            form.image_post = 'images.png'
        return render_template('recipe_page.html', form=form, posts=random_posts, profile=profile)
    else:
        return render_template('reciepe_page.html')

@app.route("/recipe")
def rec():
    
    return render_template('recipe_page.html', posts=sample_size)

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
