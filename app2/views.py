from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app.forms import LoginForm, RegForm, ChangePassForm
from app.models import User
from app.firedata import db

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        doc_ref = db.collection('users').document(form.username.data)
        user = User(form.username.data)
        if doc_ref.get().to_dict() is None or not User(form.username.data).check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegForm()
    if form.validate_on_submit():
        doc_ref = db.collection('users').document(form.username.data)
        if doc_ref.get().to_dict() is not None:
            flash('Username already taken')
            return redirect(url_for('register'))
        doc_ref.set({'name':'', 'pass_hash':'', 'cars':[], 'rentals':[]})
        user = User(form.username.data)
        user.set_name(form.name.data)
        user.set_password(form.password.data)
        flash(f'Created account with username {form.username.data}. You may now sign in.')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('register.html', title='Sign up', form=form)

@app.route('/changepass', methods=['GET','POST'])
@login_required
def changepass():
    form = ChangePassForm()
    if form.validate_on_submit():
        current_user.set_password(form.passnew.data)
        flash('Password changed successfully.')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('changepass.html', title='Change password', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')
