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
    email = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password_form = request.form.get('password')
        myquery = {"email": email}
        user_hash_password = current_app.db.users.find_one(myquery)['password']
        if pbkdf2_sha256.verify(password_form, user_hash_password):
            session['email'] = email
            flash('Zalogowałeś się skutecznie')
            return redirect(url_for('page.index'))
        flash('Nieprawidłowe hasło lub email')
    return render_template('login.html', email=email)


@pages.route('/left-sidebar')
def left():
    return render_template('left-sidebar.html')


@pages.route('/right-sidebar')
def right():
    return render_template('right-sidebar.html')


@pages.route('/no-sidebar')
def no_sidebar():
    return render_template('no-sidebar.html')


@pages.route('/elements')
def elements():
    return render_template('elements.html')
