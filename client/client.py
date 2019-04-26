from twisted.internet import ssl, reactor, endpoints, defer, task
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver
import uuid, json, os, hashlib, time, core, logging, re, imp

py_regex = "(.+\.py)$"

# These two functions are used for importing an entire directory automatically. Used for ./modules in this case.
def modules_in_dir(path):
	result = set()
	for entry in os.listdir(path):
		if os.path.isfile(os.path.join(path, entry)):
			matches = re.search(py_regex, entry)
			if matches:
				result.add(matches.group(0))
	return result

def import_dir(path):
	for filename in sorted(modules_in_dir(path)):
		search_path = os.path.join(os.getcwd(), path)
		module_name, ext = os.path.splitext(filename)
		fp, path_name, description = imp.find_module(module_name, [search_path,])
		# This uses the lowest level module loading systems to load files pulled from a directory path.
		module = imp.load_module(module_name, fp, path_name, description)

class NSTClient(LineReceiver):
	def connectionMade(self):
		core.proto_handler.on_connect(self)

	def lineReceived(self, line):
		jsonLine = json.loads(line)
		# server tells the client to store the token
		core.proto_handler.handle_line(line, self)


class NSTClientFactory(ClientFactory):
    protocol = NSTClient

    def clientConnectionFailed(self, connector, reason):
        logging.error(f"Connection failed {reason.getErrorMessage()}")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        logging.error(f"Connection lost: {reason.getErrorMessage()}")
        reactor.stop()

def main():
	logging.basicConfig(level=logging.DEBUG,filemode="w")
	#logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
	logFormatter = logging.Formatter('[%(asctime)s - %(levelname)s] [%(filename)s:%(lineno)s - %(funcName)s() - %(threadName)s] %(message)s')
	rootLogger = logging.getLogger()
	# remove the default logger
	rootLogger.handlers = []
	# Connects to the output.
	fileHandler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath( __file__ )), "client.log"))
	fileHandler.setFormatter(logFormatter)
	rootLogger.addHandler(fileHandler)

	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	rootLogger.addHandler(consoleHandler)

	core.init()

	# Automatically loads all .py files as modules from ./modules.
	import_dir("modules")
	
	factory = NSTClientFactory()
	security_form = "with certificate verification" if core.config['client']['tls_verify'] else "without certificate verification"
	logging.info(f"Connecting reactor to port {core.config['client']['address']}:{core.config['client']['port']} {security_form}.")
	reactor.connectSSL(core.config['client']['address'], core.config['client']['port'], factory, ssl.CertificateOptions(verify=core.config['client']['tls_verify']))
	logging.info("Running the reactor.")
	reactor.run()

if __name__ == '__main__':
	main()