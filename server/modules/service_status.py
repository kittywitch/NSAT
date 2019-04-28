# external
import logging, json, threading
# internal
import core

@core.add_timer(60)
def request_status():
	for server in core.servers:
		logging.info(f"Sent status update request to {server._peer.host}:{server._peer.port}")
		core.socket_send(server, json.dumps({
			"action":"update_status"
		}))
	repeat_timer = threading.Timer(60, request_status)
	repeat_timer.daemon = True
	repeat_timer.start()

@core.add_action("receive_status")
def receive_status(data, server):
	if core.capabilities["sms"]:
		pass
	if core.capabilities["pushover"]:
		pass
	print(data)

@core.add_action("ssh_login")
def ssh_login_event(data, server):
	logging.info(f"Connection as \"{data['user']}@{data['hostname']}\" from \"{data['ip']}:{data['port']}\".")