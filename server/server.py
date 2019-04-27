# external
from twisted.internet import protocol, endpoints, error
from twisted.protocols import basic
import logging, json
# internal
import core

# unserialises the JSON recieved
def deserialise(line, server):
		try:
			data = json.loads(line)
			if core.config.server.debug:
				logging.debug(f"Received \"{data}\" from \"{server._sockaddr}\".")
			return data
		except Exception as e:
			logging.error(f"Received \"{line}\" from \"{server._sockaddr}\" is not valid JSON.")
			logging.error(f"Error: \"{e}\".")
			return e

# Class Definitions for Twisted
class NSTServer(basic.LineReceiver):
	# Messages from here will be marked "NSTServer".
	def connectionMade(self):
		core.servers.append(self)
		self._peer = self.transport.getPeer()
		self._sockaddr = f"{self._peer.host}:{self._peer.port}"
		logging.info(f"Client connected from {self._sockaddr}.")

	def connectionLost(self, reason):
		if reason.type == error.ConnectionAborted:
			logging.error("Connection aborted by server.")
		elif reason.type == error.ConnectionLost:
			logging.error("Connection lost.")
		elif reason.type == error.ConnectionDone:
			logging.error("Connection closed cleanly.")
		core.servers.remove(self)

	def lineReceived(self, line):
		# takes the JSON and turns it into a python dict OR returns the error
		unsafe_data = deserialise(line, self)
		# checking if the type returned is a dictionary and not an exception
		if isinstance(unsafe_data, dict):
			data = unsafe_data
		else:
			return
		# action checking
		unsafe_action = core.get_action(data["action"])
		if callable(unsafe_action):
			action = unsafe_action
			action(data, self)
		else:
			return

class NSTServerFactory(protocol.Factory):
	protocol = NSTServer