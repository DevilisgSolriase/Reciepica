from __init__ import app, db, bcrypt
from flask import Flask, render_template, flash, redirect, url_for, request
from forms import RegistrationForm, LoginForm
from models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/home")
def home():
    return render_template('main_page.html')

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

@app.route("/Profile")
def Prof():
    return render_template('profile.html')

@app.route("/Profile personal")
@login_required
def Prof_per():
    return render_template('profile_personal.html')

@app.route("/recipe")
def rec():
    return render_template('recipe_page.html')

@app.route("/Forgot password")
def forg():
    return render_template('forgotPassword.html')
