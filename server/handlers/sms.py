from twilio.rest import Client
import core, logging

def init():
	client = Client(core.config["twilio"]["id"], core.config["twilio"]["token"])
	logging.info("Initialised.")

def notify_sms(msg_txt):
	msg = client.messages.create(
	    to=core.config["twilio"]["to"],
	    from_=core.config["twilio"]["from"],
	    body=msg_txt
	)
	return msg

def notify_call():
	# TODO: Implement TwiML service backend
	call = client.calls.create(
	    to=core.config["twilio"]["to"],
	    from_=core.config["twilio"]["from"],
	    url="http://demo.twilio.com/docs/voice.xml"
	)
	return call