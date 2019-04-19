import mod
from server import add_action

@add_action("hi")
def hello_world(data, server):
	if data["data"] == "testing, hello!":
		server.sendLine("hiya!".encode('utf8'))
		print("Server >> %s:%s: %s" % (server._peer.host, server._peer.port, "hiya!"))

@add_action("register")
def register_client(data, server):
	peer = "%s:%s" % (server._peer.host, server._peer.port)
	user_input = input("Allow registration for client %s (yes/no)? " % peer)
	if user_input == "yes":
		to_send = "{\"action\":\"enroll_token\", \"token\":\"%s\"}" % str(data["token"])
		server.sendLine(to_send.encode('utf8'))
		mod.add_token(data["uuid"], data["token"])
		print("[RegisterClient] Registered client for %s." % peer)
	elif user_input == "no":
		server.sendLine("{\"action\":\"reject\"}".encode('utf8'))
		mod.err_handler.handle_error("RegisterClient", "User not allowed to register.", server)


@add_action("reestablish")
def reestablish_client(data, server):
	peer = "%s:%s" % (server._peer.host, server._peer.port)
	token = data["token"]
	if peer in mod.token_db:
		if mod.token_db["peer"] == token:
			pass
		else:
			mod.err_handler.handle_error("ReestablishClient", "Token not valid for peer.", server)
	else:
		mod.err_handler.handle_error("ReestablishClient", "Peer not established.", server)