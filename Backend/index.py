from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__,template_folder='../Frontend/templates', static_url_path='/static')

app.config['SECRET_KEY'] = 'c7ec680eb5c98b3c720a90f6732e05cc'

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
        return redirect(url_for('Login'))
    return render_template('registration.html', form=form)

@app.route("/Profile")
def Prof():
    return render_template('Profile.html')

@app.route("/Profile personal")
def Prof_per():
    return render_template('profile_personal.html')

@app.route("/recipe")
def rec():
    return render_template('recipes_oage.html')

@app.route("/Forgot password")
def forg():
    return render_template('forgotPassword.html')


if __name__ == '__main__':
    app.run(debug=True)
    

