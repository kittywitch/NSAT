import core

@core.add_action("hi")
def hello_world(data, server):
	if data["data"] == "testing, hello!":
		core.socket_send(server, "hiya!")
		print("Server >> %s:%s: %s" % (server._peer.host, server._peer.port, "hiya!"))