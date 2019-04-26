import core, logging, json

@core.add_action("update_status")
def send_status(data, client):
	core.socket_send(client, json.dumps({
		"action":"receive_status"
	}))
