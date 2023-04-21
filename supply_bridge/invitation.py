from supply_bridge.models import Invitation, User, OrderGroup


def check_connection(user, group):
	group = OrderGroup.get(group)
	user = User.get(user)
	status = {}
	if user in group.members:
		print("Connected")
		status = {
			"status":True,
			"text": '<span class="px-1">Connected</span> <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
			"style":"btn-disabled text-success"}
	else:
		# Check if user has invite
		if Invitation.query.filter_by(group_id=group.id, receiver_id=user.id).first() is None:
			print("No Invites")
			status = {
				"status": None,
				"text": "Connect",
				"style": "text-white bg-gradient-to-r from-purple-800 to-green-500 hover:from-purple-500 hover:to-green-400 connect"}
		else:
			# if not display connect button
			print("No Connection Yet")
			status = {
				"status":False,
				"text":"Request has been sent. Waiting for Response",
				"style":"btn-disabled text-primary animate-pulse"}
	return status


#check for user groups
# check for user invitations

