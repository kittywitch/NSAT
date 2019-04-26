# external
from twisted.internet import endpoints, defer, task
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver
import logging, json
# internal
import core

class NSTClient(LineReceiver):
	def connectionMade(self):
		core.proto_handler.on_connect(self)

	def lineReceived(self, line):
		jsonLine = json.loads(line)
		core.proto_handler.handle_line(line, self)


class NSTClientFactory(ClientFactory):
    protocol = NSTClient

    def clientConnectionFailed(self, connector, reason):
        logging.error(f"Connection failed {reason.getErrorMessage()}")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        logging.error(f"Connection lost: {reason.getErrorMessage()}")
        reactor.stop()