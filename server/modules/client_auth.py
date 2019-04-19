import core

@core.add_action("register")
def register_client(data, server):
	# This implements the two actions, enroll_token and reject and their JSON structures.
	peer = "%s:%s" % (server._peer.host, server._peer.port)
	user_input = input("Allow registration for client %s (yes/no)? " % peer)
	if user_input == "yes":
		core.socket_send(server, "{\"action\":\"enroll_token\", \"token\":\"%s\"}" % str(data["token"]))
		core.add_token(data["uuid"], data["token"])
		print("[RegisterClient] Registered client for %s." % peer)
	elif user_input == "no":
		core.socket_send(server, "{\"action\":\"reject\"}")
		core.err_handler.handle_error("RegisterClient", "User not allowed to register.", server)


@core.add_action("reestablish")
def reestablish_client(data, server):
	# This allows a client that already has enrolled a token to reestablish a tokenized connection.
	peer = "%s:%s" % (server._peer.host, server._peer.port)
	token = data["token"]
	if peer in core.token_db:
		if core.token_db["peer"] == token:
			pass
		else:
			core.err_handler.handle_error("ReestablishClient", "Token not valid for peer.", server)
	else:
		core.err_handler.handle_error("ReestablishClient", "Peer not established.", server)