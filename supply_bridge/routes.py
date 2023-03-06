from flask import Flask, flash, redirect, render_template, url_for, request, send_from_directory, jsonify
from werkzeug.urls import url_parse
from supply_bridge import app, db
from supply_bridge.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, MessageForm
from supply_bridge.models import User, Group, Role, Notification
from supply_bridge.email import send_password_reset_email
from flask_security import roles_accepted
import json
import phonenumbers
from phonenumbers import geocoder
from sqlalchemy_utils import PhoneNumber
from flask_login import login_user, login_required, current_user, logout_user
import os
from datetime import datetime
 
 






def get_or_create(model, **kwargs):
    """SqlAlchemy implementation of Django's get_or_create.
    """
    session = db.session()
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        phone_number = phonenumbers.parse(form.phone.data)
        country_prefix = geocoder.region_code_for_number(phone_number)
        user = User(
            firstname=form.lastname.data,
            lastname=form.firstname.data,
            email=form.email.data,
            phone_number=PhoneNumber(f'0{phone_number.national_number}', country_prefix),)
        user.set_password(form.password.data)
        if User.query.filter_by(email=user.email).first() is None:
            group = get_or_create(Group, name="Customer")[0]
            role = get_or_create(Role, name="Customer")[0]
            user.groups.append(group)
            user.roles.append(role)
            db.session.add(user)
            db.session.commit()
            flash("Your Account has been created! You are now able to login", 'success')
            return redirect(url_for('login'))
        else:
            flash(
                "This Account has already been created! You'll need to try again ", 'warning')
            return redirect(url_for('register'))
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('user', email=user.email)
            return redirect(next_page)
        else:
            flash('Login unsuccessful. Please check Username and Password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html', title="login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<email>')
@login_required
def user(email):
    user = User.query.filter_by(email=email).first_or_404()
    return render_template('user.html', user=user,)


@app.route('/password_reset', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template("reset_password_request.html",
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@roles_accepted("Admin")
@login_required
def send_message(recipient):
    user = User.query.filter_by(email=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit() and user:
        n = Notification(name='Urgent Message!!', payload_json=json.dumps(form.message.data), reciever=user)
        db.session.add(n)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', email=current_user.email))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=recipient)


@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter( Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': datetime.fromtimestamp(n.timestamp)
    } for n in notifications])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
