from supply_bridge.models import Invitation, Order, User, OrderGroup


def check_coonnection(id, group_id):
	group = OrderGroup.get(group_id)
	user = User.get(id)
	print(group, user)
	return True



