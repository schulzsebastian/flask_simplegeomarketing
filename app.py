from flask import Flask, render_template, redirect, request, url_for, g
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, current_user, login_required, login_user, logout_user

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object('config.LocalConfig')
db = SQLAlchemy(app)
from models import *

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET','POST'])
def login():
    if g.user.is_authenticated:
        return redirect(url_for('map'))
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    password = request.form['password']
    registered_user = User.query.filter_by(username=username).first()

    if registered_user is None:
        return redirect(url_for('login'))
    if bcrypt.check_password_hash(registered_user.password, password):
        login_user(registered_user)
        return redirect(url_for('map'))

    return redirect(url_for('login'))

@app.route('/')
@app.route('/map')
def map():
    if not g.user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('map.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
