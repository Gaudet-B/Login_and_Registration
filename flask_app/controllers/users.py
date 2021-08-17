from flask import app
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/register/verify", methods=['POST'])
def verify_registration():
    pw_hash = bcrypt.generate_password_hash(request.form['password_input'])
    data = {
        "first_name": request.form['first_name_input'],
        "last_name": request.form['last_name_input'],
        "email":request.form['email_input'],
        "password": pw_hash
    }
    check = User.validate_user(request.form)
    print(f'oooooooooooo {check}')
    if not check:
        flash("sorry, we were unable to validate your registration.")
        print(f"PpPpPpP: ----------------")
        return redirect("/register")
    User.new_user(data)
    return redirect("/success")

@app.route("/success")
def success():
    users = User.get_all()
    print(f"print: {users}")
    return render_template("success.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login/verify")
def verify_login():
    return redirect("/success")

@app.route("/logout")
def logout():
    return redirect("")