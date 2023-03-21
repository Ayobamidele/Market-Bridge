from flask import flash, redirect, render_template, url_for, request, send_from_directory, request
from werkzeug.urls import url_parse
from supply_bridge import app, db
from supply_bridge.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, MessageForm, user_edit
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
import sqlalchemy.exc as e 



def update_or_create(model, is_existed_keys: list = [],   **kwargs):
    session = db.session()
    query = None
    old = None
    obj = None
    new_kwargs = kwargs if len(is_existed_keys) == 0 else {}
    created_by_key = is_existed_keys or []
    for key in created_by_key:
        new_kwargs[key] = kwargs[key]
    try:
        query = session.query(model).filter_by(**new_kwargs)
        old = query.one()
    except e.NoResultFound:
        obj = model(**kwargs)
        try:
            session.add(obj)
            session.flush()
        except e.IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one(), False
        return obj, True
    try:
        # need update
        query.update(kwargs)
        session.flush()
        session.commit()
    except e.IntegrityError:
        session.rollback()
    return old, False


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
    return render_template("home.html",user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", title="About", user=current_user)


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
            Notification(name='Welcome to Market Bridge',
                         payload_json=json.dumps(
                        f"Welcome {user.firstname}, Plan wisely withe market bridge to get the best out of all products being delivered."),
                        reciever=user).save()
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


@app.route('/user/<email>', methods=['GET', 'POST'])
@login_required
def user(email):
    user = User.query.filter_by(email=email).first_or_404()
    print(user.is_admin())
    return render_template('user.html', user=user, )

@app.route('/user/<email>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(email):
    user = User.query.filter_by(email=email).first_or_404()
    form = user_edit(obj=user)
    if request.method == 'POST':
        if form.cancel.data:
            return redirect(url_for('user', email=email))
        elif form.save.data:
            print(form.data, form.validate())
            # phone_number = phonenumbers.parse(form.phone_number.data)
            # country_prefix = geocoder.region_code_for_number(phone_number)
            # print(phone_number)
            # # phone_number = phonenumbers.parse(form.phone_number.data)
            # # country_prefix = geocoder.region_code_for_number(phone_number)
            # # phone_number=PhoneNumber(form.phone_number.data, country_prefix
            # # new_number = PhoneNumber(form.phone_number.data, country_prefix)
            # # form.data['phone_number'] =
            # # print(form.phone_number.data, user.phone_country_code)
            # updated_user = User.query.filter_by(email=email).update(values=dict(form.data), synchronize_session=False)
            # a = update_or_create(User,is_existed_keys=['id'],id=user.id,firstname=form.lastname.data,
            #                     lastname=form.firstname.data,
            #                     email=form.email.data, )
            return redirect(url_for('user', email=email))
    return render_template('user_edit.html', user=current_user, form=form, country=user.phone_country_code)

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
                           form=form, recipient=recipient, user=current_user)


@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    user_notifications = current_user.notifications.filter( Notification.timestamp > since).order_by(Notification.timestamp.asc())
    user_notifications = ([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': datetime.fromtimestamp(n.timestamp).strftime("%Y/%m/%d  %H:%M"),
        'read': "100" if n.read == False else "50",
        'id': n.id
    } for n in user_notifications])
    print(user_notifications)
    return render_template('notifications.html', title=f'notifications-{current_user.firstname}', notifications=user_notifications,
                           notification_display="none",user=current_user)

@app.route('/notification/<id>')
@login_required
def get_notification(id):
    user_notification = [{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': datetime.fromtimestamp(n.timestamp).strftime("%Y/%m/%d  %H:%M"),
        'read': n.read,
        'id': n.id,
        'notification':n
    } for n in current_user.notifications.filter_by(id=id).all() ][0]
    user_notification['notification'].read = True
    user_notification['notification'].save()
    return render_template('notification.html', title=f"notifications-{user_notification['name']}", notification=user_notification,
                           user=current_user)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
