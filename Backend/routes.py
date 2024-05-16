from __init__ import app, db, bcrypt
from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from models import User, Post

@app.route("/home")
def home():
    return render_template('main_page.html')

@app.route("/Login", methods=['GET', 'POST'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Account Created for {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', form = form)

@app.route("/Register", methods=['GET', 'POST'])
def Reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created!')
        return redirect(url_for('Login'))
    return render_template('registration.html', form=form)

@app.route("/Profile")
def Prof():
    return render_template('profile.html')

@app.route("/Profile personal")
def Prof_per():
    return render_template('profile_personal.html')

@app.route("/recipe")
def rec():
    return render_template('recipe_page.html')

@app.route("/Forgot password")
def forg():
    return render_template('forgotPassword.html')
