from flask import Blueprint, render_template, request, session, \
    redirect, url_for, flash, current_app
from passlib.hash import pbkdf2_sha256

pages = Blueprint('page', __name__, static_folder='static', template_folder='templates')


@pages.route('/')
def index():
    return render_template('index.html', email=session.get('email'))


@pages.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        new_user = {
            'email': email,
            'password': password
        }
        current_app.db.users.insert_one(new_user)
        flash("Successfully signed up.")
        session['email'] = email
        return redirect(url_for('page.index'))
    return render_template('signup.html')


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
