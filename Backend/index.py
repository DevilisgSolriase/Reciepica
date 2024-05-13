from flask import Flask, render_template

app = Flask(__name__,template_folder='../Frontend/templates')

@app.route("/home")
def home():
    return render_template('main_page.html')

@app.route("/Login")
def Login():
    return render_template('login.html')

@app.route("/Register")
def Reg():
    return render_template('registration.html')

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
    

