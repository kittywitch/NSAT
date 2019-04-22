import http.client, urllib
import core

def init():
	client = http.client.HTTPSConnection("api.pushover.net:443")


def notify_po(msg):
	client.request("POST", "/1/messages.json",
	urllib.parse.urlencode({
		"token": core.cfg_handler.config["pushover"]["token"],,
		"user": core.cfg_handler.config["pushover"]["user"],,
		"message": msg,
	}), { "Content-type": "application/x-www-form-urlencoded" })
	client.getresponse()