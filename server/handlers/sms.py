# external
from twilio.rest import Client
import logging
# internal
import core

def init():
	try:
		client = Client(core.config.twilio.id, core.config.twilio.token)
		if hasattr(core.config.twilio, "in") and hasattr(core.config.twilio, "out") and core.config.twilio.id != None and core.config.twilio.token != None and core.config.twilio.in_n != None and core.config.twilio.out_n != None:
			logging.info("Config required for Twilo provided. Twilio support enabled.")
			return True
		else:
			logging.info("Config required for Twilio not provided. Twilio support disabled.")
			return False
	except:
		return False

def notify_sms(msg_txt):
	if core.capabilities["sms"]:
		msg = client.messages.create(
		    to = core.config.twilio.out_n,
		    from_ = core.config.twilio.in_n,
		    body = msg_txt
		)
		logging.debug(msg)
		return msg

# TODO: Implement TwiML service backend
def notify_call():
	if core.capabilities["sms"]:
		call = client.calls.create(
		    to = core.config.twilio.out_n,
		    from_ = core.config.twilio.in_n,
		    url = "http://demo.twilio.com/docs/voice.xml"
		)
		logging.debug(msg)
		return call