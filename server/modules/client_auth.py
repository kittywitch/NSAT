# external
import logging, json
# internal
import core, handlers.pushover, handlers.sms

@core.add_action("register")
def register_client(data, server):
	# This implements the two actions, enroll_token and reject and their JSON structures.
	peer = f"{server._peer.host}:{server._peer.port}"
	user_input = input(f"Allow registration for client {peer} (yes/no)? ")
	if user_input == "yes":
		core.socket_send(server, json.dumps({
			"action":"enroll_token",
			"uuid":data["uuid"],
			"token":data["token"]
		}))
		output = f"Registered token UUID \"{data['uuid']}\" with token \"{data['token']}\" for peer \"{peer}\"."
		handlers.pushover.notify(output)
		handlers.sms.notify_sms(output)
		logging.info(output)
		core.add_token(data["uuid"], data["token"])
	elif user_input == "no":
		core.socket_send(server, json.dumps({
			"action":"reject"
		}))
		output = f"Peer \"{peer}\" not allowed to register with UUID \"{data['uuid']}\" and token \"{data['token']}\"."
		handlers.pushover.notify(output)
		handlers.sms.notify_sms(output)
		logging.error(output)


@core.add_action("reestablish")
def reestablish_client(data, server):
	# This allows a client that already has enrolled a token to reestablish a tokenized connection.
	#peer = "%s:%s" % (server._peer.host, server._peer.port)
	peer = f"{server._peer.host}:{server._peer.port}"
	uuid = data["uuid"]
	token = data["token"]
	if uuid in core.token_db:
		if core.token_db[uuid] == token:
				output = f"UUID \"{uuid}\" and token \"{token}\" valid for peer \"{peer}\"."
				handlers.pushover.notify(output)
				handlers.sms.notify_sms(output)
				logging.info(output)
				core.socket_send(server, json.dumps({
				"action":"authorised"
			}))
		else:
			output = f"UUID \"{uuid}\" and token \"{token}\" are not valid for peer \"{peer}\"."
			handlers.pushover.notify(output)
			handlers.sms.notify_sms(output)
			logging.error(output)
	else:
		handlers.pushover.notify(output)
		handlers.sms.notify_sms(output)
		logging.error(output)