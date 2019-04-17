import mod
from server import add_action

@add_action("hi")
def hello_world(data, server):
	if data["data"] == "testing, hello!":
		server.transport.write("hiya!")
		print("Server >> %s:%s: %s" % (server._peer.host, server._peer.port, "hiya!"))