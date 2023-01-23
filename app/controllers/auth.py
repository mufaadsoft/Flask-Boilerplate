from app import db
from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

#model
from app.models.user import User

auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash(message="Oops invalid user", category="err")
        else:
            if check_password_hash(user.password, password=password):
                login_user(user)
                return redirect(url_for("auth.secure"))
            else:
                flash(message="Incorrect Password", category="err")
    return render_template('auth/login.html')


@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'), method="pbkdf2:sha256", salt_length=2)
        user = User(name=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("auth.secure"))
    return render_template('auth/register.html')


@auth.route('/secure')
@login_required
def secure():
    return f'Your logged in <a href="{url_for("auth.logout")}">Logout</a>'


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("auth.login"))