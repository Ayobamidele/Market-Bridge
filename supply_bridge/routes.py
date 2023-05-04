from flask import (
    flash,
    redirect,
    render_template,
    url_for,
    send_from_directory,
    request
)
from werkzeug.urls import url_parse
from supply_bridge import app, db
from supply_bridge.forms import (
    LoginForm,
    RegistrationForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    MessageForm,
    UserEdit,
    PhoneChangeForm,
    MeasureForm
)
from supply_bridge.models import User, Group, Role, Notification, Order, OrderStatus, Orderchema, ItemSchema, Measure
from supply_bridge.email import send_password_reset_email
from supply_bridge.decorators import authorise_order_access, unauthenticated_only
from supply_bridge.invitation import check_connection
from flask_security import roles_accepted
import json
import phonenumbers
from phonenumbers import geocoder
from sqlalchemy_utils import PhoneNumber
from flask_login import login_user, login_required, current_user, logout_user
import os
from datetime import datetime
import sqlalchemy.exc as e
import emojis
import random

def get_or_create(model, **kwargs):
    """SqlAlchemy implementation of Django's get_or_create."""
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
    return render_template("home/home.html", user=current_user, emojis=emojis)


@app.route("/about")
def about():
    return render_template(
        "home/about.html", title="About", user=current_user, emojis=emojis
    )

@app.route("/register", methods=["GET", "POST"])
@unauthenticated_only
def register():
    """
    It takes the phone number from the form, parses it, gets the country code, creates a user, sets the
    password, sets the username, checks if the user exists, if not, it creates a group, role, appends
    the group and role to the user, saves the user, sends a notification to the user, and redirects to
    the login page
    :return: a tuple of the form (object, created), where object is the retrieved or created object and
    created is a boolean specifying whether a new object was created.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        phone_number = phonenumbers.parse(form.phone.data)
        country_prefix = geocoder.region_code_for_number(phone_number)
        user = User(
            firstname=form.lastname.data,
            lastname=form.firstname.data,
            email=form.email.data,
            phone_number=PhoneNumber(
                f"0{phone_number.national_number}", country_prefix
            ),
        )
        user.set_password(form.password.data)
        user.set_username()
        if User.query.filter_by(email=user.email).first() is None:
            group = get_or_create(Group, name="Customer")[0]
            role = get_or_create(Role, name="Customer")[0]
            user.groups.append(group)
            user.roles.append(role)
            user.save()
            flash("Your Account has been created! You are now able to login", "success")
            Notification(
                name="Welcome to Market Bridge",
                payload_json=json.dumps(
                    f"Welcome {user.firstname}, Plan wisely withe market bridge to get the best out of all products being delivered."
                ),
                reciever=user,
            ).save()
            return redirect(url_for("login"))
        else:
            flash(
                "This Account has already been created! You'll need to try again ",
                "warning",
            )
            return redirect(url_for("register"))
    return render_template("auth/registration/register.html", title="Register", emojis=emojis, user=current_user, form=form)


@app.route("/login", methods=["GET", "POST"])
@unauthenticated_only
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Hello")
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("user")
            flash(f"Login successful. Welcome Back {user.username}", "success")
            return redirect(next_page)
        else:
            flash("Login unsuccessful. Please check Username and Password", "danger")
            return redirect(url_for("login"))
    return render_template("auth/login/login.html", title="login", user=current_user, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def user():
    print(dir(current_user))
    if request.method == "POST" and request.json.get("create"):
        new_order = Order(
            title=f"Order-{random.randint(2383385933, 2345678918376829)}",
            contributors=[current_user],
            content=f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}",
            owner=current_user.id,
        )
        new_order.save()
        return (
            redirect(
                url_for(
                    "create_order",
                    username=current_user.username,
                    title=new_order.title,
                ),
                code=307,
            ),
            307,
        )
    # user_orders = current_user.orders
    limit = 6
    user_order = [
        {
            "title": o.title,
            "content": o.content,
            "status": o.status.value,
            "date_created": o.date_created.strftime("%Y/%m/%d  %H:%M"),
            "contributors": o.contributors,
            "suppliers": o.suppliers,
            "link": url_for(
                "create_order", username=o.get_owner().username, title=o.title
            ),
        }
        for o in current_user.orders
    ]
    # user_orders = OrderTable(user_order)
    # print(user_orders.tr(user_orders))
    return render_template(
        "profile/profile.html", user=current_user, emojis=emojis, orders=user_order, limit=limit
    )


@app.route("/profile/settings", methods=["GET", "POST"])
@login_required
def edit_user():
    form = UserEdit(obj=current_user)
    if request.method == "POST":
        if form.cancel.data:
            return redirect(url_for("user"))
        elif form.save.data:
            if form.validate_on_submit():
                current_user.update(
                    lastname=form.lastname.data,
                    firstname=form.firstname.data,
                    username=form.username.data,
                    email=form.email.data,
                )
                flash("Successfully updated your profile !!!", 'success')
                return redirect(url_for("user"))
            else:
                flash("Incomplete or wrong format", 'warning')
    return render_template(
        "profile/user_edit.html",
        user=current_user,
        form=form,
        emojis=emojis,
    )


@app.route("/profile/settings/phone", methods=["GET", "POST"])
@login_required
def change_user_phone():
    form = PhoneChangeForm(obj=current_user)
    if request.method == "POST":
        print(form)
        if form.cancel.data:
            return redirect(url_for("user"))
        elif form.validate_on_submit():
            phone_number = phonenumbers.parse(form.phone.data, "NG")
            country_prefix = geocoder.region_code_for_number(phone_number)
            current_user.update(
                phone_number=PhoneNumber(f"0{phone_number.national_number}", country_prefix)
            )
            flash("Successfully changed your phone number !!!", 'success')
            return redirect(url_for("user"))
        else:
            flash("Incomplete or wrong format", 'warning')
    return render_template(
        "profile/change_phone.html",
        user=current_user,
        form=form,
        emojis=emojis,
    )


# print(form.data, form.validate())
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
# a = update_or_create(
#     User,
#     is_existed_keys=["id"],
#     id=user.id,
#     lastname=form.lastname.data,
#     firstname=form.firstname.data,
#     username=form.username.data,
#     email=form.email.data,
# )
# db.session().commit()


@app.route("/password_reset", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        validated_user = User.query.filter_by(email=form.email.data).first()
        if validated_user:
            send_password_reset_email(validated_user)
        flash("Check your email for the instructions to reset your password")
        return redirect(url_for("login"))
    return render_template(
        "auth/password/reset_password_request.html", title="Reset Password", user=current_user, form=form
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if not current_user.is_authenticated:
        authenticated_user = User.verify_reset_password_token(token)
        if not authenticated_user:
            return redirect(url_for('index'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            authenticated_user.set_password(form.password.data)
            db.session.commit()
            flash("Your password has been reset.")
            return redirect(url_for("login"))
        return render_template("auth/password/reset_password.html", form=form, user=current_user)
    return redirect(url_for("index"))


@app.route("/send_message/<recipient>", methods=["GET", "POST"])
@roles_accepted("Admin")
@login_required
def send_message(recipient):
    recipient = User.query.filter_by(email=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit() and recipient:
        n = Notification(
            name="Urgent Message!!",
            payload_json=json.dumps(form.message.data),
            reciever=recipient,
        )
        db.session.add(n)
        db.session.commit()
        flash("Your message has been sent.")
        return redirect(url_for("user"))
    return render_template(
        "send_message.html",
        title="Send Message",
        form=form,
        recipient=recipient,
        user=current_user,
    )


@app.route("/notifications")
@login_required
def notifications():
    since = request.args.get("since", 0.0, type=float)
    user_notifications = current_user.notifications.filter(
        Notification.timestamp > since
    ).order_by(Notification.timestamp.asc())
    user_notifications = [
        {
            "name": n.name,
            "data": n.get_data(),
            "timestamp": datetime.fromtimestamp(n.timestamp).strftime(
                "%Y/%m/%d  %H:%M"
            ),
            "read": "100" if n.read is False else "50",
            "id": n.id,
        }
        for n in user_notifications
    ]
    print(user_notifications)
    return render_template(
        "notifications.html",
        title=f"notifications-{current_user.firstname}",
        notifications=user_notifications,
        user=current_user,
        emojis=emojis,
    )


@app.route("/notification/<id>")
@login_required
def get_notification(id):
    user_notification = [
        {
            "name": n.name,
            "data": n.get_data(),
            "timestamp": datetime.fromtimestamp(n.timestamp).strftime(
                "%Y/%m/%d  %H:%M"
            ),
            "read": n.read,
            "id": n.id,
            "notification": n,
        }
        for n in current_user.notifications.filter_by(id=id).all()
    ][0]
    user_notification["notification"].read = True
    user_notification["notification"].save()
    return render_template(
        "notification.html",
        title=f"notifications-{user_notification['name']}",
        notification=user_notification,
        user=current_user,
        emojis=emojis,
    )


@app.route("/order/<username>/<title>", methods=["GET", "POST"])
@login_required
@authorise_order_access
def create_order(username, title):
    from urllib.parse import quote,unquote
    limit = 6
    owner = User.query.filter_by(username=username).first()
    order = Order.query.filter_by(title=title, owner=owner.id).first()
    edit = order.can_edit(current_user)
    # print(unquote(url_for('get_order', title=order.title, username=order.get_owner().username)))
    if request.method == "POST" and request.json['type'] == "measure":
        data = request.json
        form = MeasureForm()
        form.name.data = data['name']
        if form.validate():
            obj = Measure.create(name=data['name'])
            flash(f"Created {obj.name} !!!","success")
            return {"text": obj.name, "update": False}, 200
        else:
            return {"text": form.errors['name'][0] , 'update': True, 'name': data['name']},200
    return render_template(
        "create_list.html",
        emojis=emojis,
        user=current_user,
        edit=edit,
        order=order,
        limit=limit,
    )

@app.route("/order/<username>/<title>/items", methods=["GET", "POST"])
@login_required
@authorise_order_access
def get_order(username, title):
    owner = User.query.filter_by(username=username).first()
    order = Order.query.filter_by(title=title, owner=owner.id).first()
    order_data = Orderchema().dump(order)
    data = {
                **order_data,
				"status": True,
                "edit": order.can_edit(current_user),
                "limit": 6
            }
    print(data)
    return data


@app.route("/order/<username>/<title>/edit", methods=["GET", "POST"])
@login_required
@authorise_order_access
def edit_order(username, title):
    owner = User.query.filter_by(username=username).first()
    order = Order.query.filter_by(title=title, owner=owner.id).first()
    
    if not order.can_edit(current_user):
        return redirect(url_for("forbidden"))
        
    if request.method == "POST":
        order.title = request.form.get("title")
        order.description = request.form.get("description")
        
        db.session.commit()
        flash("Order updated successfully.","success")
        return redirect(url_for("create_order", username=username, title=order.title))
    
    return render_template("edit_order.html", order=order,emojis=emojis,user=current_user,limit=6)

@app.route("/orders/<username>/<title>/assign", methods=["GET", "POST"])
@login_required
def assign_items(username, title):
    owner = User.query.filter_by(username=username).first()
    order = Order.query.filter_by(title=title, owner=owner.id).first()

    if request.method == "POST":
        assigned_items = request.form.getlist("assigned_items")

        order.assigned_items.clear()

        for item_id in assigned_items:
            item = Order.query.get(item_id)
            order.assigned_items.append(item)

        db.session.commit()
        flash("Items assigned successfully.")
        return redirect(url_for("create_order", username=username, title=title))

    # Get the items that can be assigned to the order
    available_items = Order.query.filter(Order.vendor == current_user).all()

    return render_template(
        "assign_items.html",
        order=order,
        available_items=available_items,
    )



@app.route("/<username>/<title>/friends/market", methods=["GET", "POST"])
@login_required
@authorise_order_access
def friends(username, title):
    owner = User.query.filter_by(username=username).first()
    order = Order.query.filter_by(title=title, owner=owner.id).first()
    data = User.query.filter(User.id.not_in([current_user.id]))
    result = []
    group = order.get_group()
    for user in data:
        user_data = {"user" : user, "connection":check_connection(user.id, order.group.id)}
        result.append(user_data)
    if request.method == "POST" and request.json.get("connect"):
        user = request.json.get('user')
        if check_connection(user, order.group.id)['status'] == None:
            # Working on setting up invitation page for users
            order.send_invitation(current_user.id, int(user))
            return {
				"status":False,
				"text":"Request has been sent. Waiting for Response",
				"style":"btn flex flex-nowrap ml-auto mr-20 btn-disabled text-primary-focus animate-pulse"
                }, 200
    return render_template("home/friends.html", user=current_user, order=order, result=result)


@app.route("/order/<username>/<title>/contributors", methods=["GET", "POST"])
@login_required
@authorise_order_access
def order_contributors(username, title):
    limit = 6
    owner = User.query.filter_by(username=username).first()
    order = Order.query.filter_by(title=title, owner=owner.id).first()
    edit = order.can_edit(current_user)
    # Add user to contibutors of order by username
    if request.method == "POST" and request.json.get("add"):
        print("Testing ....")
        # invitation = Notification(
        #     name=f"Invitation to - {order.title}",
        #     payload_json=json.dumps(""),
        #     reciever=request.json.get('username'),
        # )
        # invitation.save()
        # flash("Your message has been sent.")
    return render_template("order_contributors.html", emojis=emojis,
                           user=current_user, order=order, edit=edit, limit=limit)


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.errorhandler(403)
def forbidden(error):
    return render_template("error/403_page.html"), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("error/404_page.html"), 404
