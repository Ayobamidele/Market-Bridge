# from flask_principal import Permission, RoleNeed

# admin_permission = Permission(RoleNeed('Admin'))
from functools import wraps
from flask_login import current_user
from supply_bridge.models import User, Order
from flask import redirect, abort, url_for


def authorise_order_access(f):
    @wraps(f)
    def wrap(*args, **kwargs):  # if user is not logged in, redirect to login page
        username = kwargs["username"]
        title = kwargs["title"]
        user = User.query.filter_by(username=username).first()
        order = Order.query.filter_by(title=title).first()
        if user is not None and order is not None:
            if order.has_access(current_user) and user.order_exist(title=title):
                pass
                #  return redirect(url_for("create_order", username=order.get_owner().username, title=order.title))
                # print(order.has_access(current_user), order.suppliers, order.contributors)
            else:
                abort(403)
        else:
            abort(404)
        return f(*args, **kwargs)

    return wrap
