import functools

from flask import Blueprint, render_template, request, session, \
    redirect, url_for, flash, current_app
from passlib.hash import pbkdf2_sha256

pages = Blueprint('page', __name__, static_folder='static', template_folder='templates')


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for("page.login"))

        return route(*args, **kwargs)

    return route_wrapper


@pages.route('/')
@login_required
def index():
    return render_template('index.html', email=session.get('email'))


@pages.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = {
            'email': email,
            'password': pbkdf2_sha256.hash(password)
        }
        current_app.db.users.insert_one(new_user)
        flash('Zalogowałeś się skutecznie')
        session['email'] = email
        return redirect(url_for('page.index'))
    return render_template('signup.html')


@pages.route('/login', methods=['GET', 'POST'])
def login():
    email = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        my_query = {'email': email}
        user_data = current_app.db.users.find_one({"email": email})
        if not user_data:
            flash('Login credentials not correct')
            return redirect(url_for('.login'))

        hashed_password = current_app.db.users.find_one(my_query)['password']
        if pbkdf2_sha256.verify(password, hashed_password):
            session['email'] = email
            flash('Zalogowałeś się skutecznie')
            return redirect(url_for('page.index'))
        flash('Nieprawidłowe hasło lub email')
    return render_template('login.html', email=email)


@pages.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('.login'))


@pages.route('/zamowienia')
@login_required
def zamowienia():
    email = session['email']
    return render_template('zamowienia.html', email=email)
