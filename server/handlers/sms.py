from twilio.rest import Client
import core

def init():
	print("[TwilioHandler] Initialised.")
	client = Client(core.cfg_handler.config["server"]["twilio_id"], core.cfg_handler.config["server"]["twilio_token"])

def notify_sms(msg_txt):
	msg = client.messages.create(
	    to=core.cfg_handler.config["server"]["twilio_out"],
	    from_=core.cfg_handler.config["server"]["twilio_in"],
	    body=msg_txt
	)
	return msg

def notify_call():
	# TODO: Implement TwiML service backend
	call = client.calls.create(
	    to=core.cfg_handler.config["server"]["twilio_out"],
	    from_=core.cfg_handler.config["server"]["twilio_in"],
	    url="http://demo.twilio.com/docs/voice.xml"
	)
	return call