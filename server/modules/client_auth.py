import core, logging

@core.add_action("register")
def register_client(data, server):
	# This implements the two actions, enroll_token and reject and their JSON structures.
	peer = "%s:%s" % (server._peer.host, server._peer.port)
	user_input = input(f"Allow registration for client {peer} (yes/no)? ")
	if user_input == "yes":
		core.socket_send(server, f"{{\"action\":\"enroll_token\", \"uuid\":\"{str(data['uuid'])}\", \"token\":\"{str(data['token'])}\"}}")
		core.add_token(data["uuid"], data["token"])
		logging.info(f"Registered client for {peer}.")
	elif user_input == "no":
		core.socket_send(server, "{\"action\":\"reject\"}")
		logging.error("User not allowed to register.")


@core.add_action("reestablish")
def reestablish_client(data, server):
	# This allows a client that already has enrolled a token to reestablish a tokenized connection.
	#peer = "%s:%s" % (server._peer.host, server._peer.port)
	peer = data["uuid"]
	token = data["token"]
	if peer in core.token_db:
		if core.token_db[peer] == token:
			logging.info("Token valid for peer.")
			core.socket_send(server, f"{{\"action\":\"authorised\"}}")
		else:
			logging.error("Token not valid for peer.")
	else:
		logging.error("Peer not established.")