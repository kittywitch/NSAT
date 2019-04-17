from twisted.internet import ssl, reactor, endpoints, defer, task
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver

class NSTClient(LineReceiver):
	def connectionMade(self):
		self.sendLine("{\"action\":\"hi\", \"data\":\"testing, hello!\"}")

	def lineReceived(self, line):
		print("received: "+line)

class NSTClientFactory(ClientFactory):
    protocol = NSTClient

    def clientConnectionFailed(self, connector, reason):
        print "connection failed: ", reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "connection lost: ", reason.getErrorMessage()
        reactor.stop()

def main():
	factory = NSTClientFactory()
	reactor.connectSSL('127.0.0.1', 50000, factory, ssl.CertificateOptions(verify=False))
	reactor.run()

if __name__ == '__main__':
	main()