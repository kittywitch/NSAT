# external
import http.client, urllib, logging
# internal
import core

def init():
	global client
	if hasattr(core.config.pushover, "user") and hasattr(core.config.pushover, "token") and core.config.pushover.user != None and core.config.pushover.token != None:
		client = http.client.HTTPSConnection("api.pushover.net:443")
		logging.info("Config required for Pushover provided. Pushover support enabled.")
		return True
	else:
		logging.info("Config required for Pushover not provided. Pushover support disabled.")
		return False

def notify(msg):
	if core.capabilities["pushover"]:
		client.request("POST", "/1/messages.json",
		urllib.parse.urlencode({
			"token": core.config.pushover.token,
			"user": core.config.pushover.user,
			"message": msg,
		}), { "Content-type": "application/x-www-form-urlencoded" })
		return client.getresponse()
	else:
		return None