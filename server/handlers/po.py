# external
import http.client, urllib, logging
# internal
import core

def init():
	client = http.client.HTTPSConnection("api.pushover.net:443")
	logging.info("Initialised.")

def notify_po(msg):
	client.request("POST", "/1/messages.json",
	urllib.parse.urlencode({
		"token": core.config["pushover"]["token"],
		"user": core.config["pushover"]["user"],
		"message": msg,
	}), { "Content-type": "application/x-www-form-urlencoded" })
	client.getresponse()