# external
from twisted.internet import protocol, endpoints, error
from twisted.protocols import basic
import logging
# internal
import core

# Class Definitions for Twisted
class NSTServer(basic.LineReceiver):
	# Messages from here will be marked "NSTServer".
	def connectionMade(self):
		# TODO: Session handling.
		core.servers.append(self)
		self._peer = self.transport.getPeer()
		logging.info(f"Client connected from {self._peer.host}:{self._peer.port}.")
		core.proto_handler.on_connect(self)

	def connectionLost(self, reason):
		if reason.type == error.ConnectionAborted:
			logging.error("Connection aborted by server.")
		elif reason.type == error.ConnectionLost:
			logging.error("Connection lost.")
		elif reason.type == error.ConnectionDone:
			logging.error("Connection closed cleanly.")

	def lineReceived(self, line):
		core.proto_handler.handle_line(line, self)

class NSTServerFactory(protocol.Factory):
	protocol = NSTServer