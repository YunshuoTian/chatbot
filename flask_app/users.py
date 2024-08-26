from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_app.models import Users
from flask_app import db
from sqlalchemy.exc import IntegrityError


bp = Blueprint('users', __name__)

@bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('users/signup.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            hashed_password = generate_password_hash(password)
            user = Users(username=username, password=hashed_password)

            try:
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('index'))
            except IntegrityError:
                db.session.rollback()
                flash('Username already exists', 'error')
        else:
            flash('Invalid username or password', 'error')

    return render_template('users/signup.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Users.query.filter(Users.username == username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Wrong username or password', 'error')
    return render_template('users/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))