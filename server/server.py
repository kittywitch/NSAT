#!/usr/bin/env python

# General imports.
from twisted.internet import ssl, reactor, protocol, endpoints, error
from twisted.protocols import basic
import configparser, sys, os, re, imp, logging

# Modules created for this project.
import core

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

# This is the implementation of the actual socket system using Twisted. The protocol handler is used to actually deal with things, though.
def main():
	# Sets this to overwrite ./server.log with the log file contents of this session.
	logging.basicConfig(filename="server.log",level=logging.DEBUG,filemode="w")
	#logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
	logFormatter = logging.Formatter('[%(filename)s:%(lineno)s - %(funcName)s() - %(threadName)s] %(levelname)s - %(message)s')
	rootLogger = logging.getLogger()
	# Connects to the output.
	fileHandler = logging.FileHandler("server.log")
	fileHandler.setFormatter(logFormatter)
	rootLogger.addHandler(fileHandler)

	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	rootLogger.addHandler(consoleHandler)

	# Class Definitions for Twisted
	class NSTServer(basic.LineReceiver):
		# Messages from here will be marked "NSTServer".
		def connectionMade(self):
			# TODO: Session handling.
			self._peer = self.transport.getPeer()
			logging.info("Client connected from %s:%d." % (self._peer.host, self._peer.port))
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

	# Messages from here will be marked "Main".	
	# Initialises the handlers for use elsewhere.
	core.init()

	# Automatically loads all .py files as modules from ./modules.
	import_dir("modules")

	factory = NSTServerFactory()
	logging.info(f"Binding reactor to port {core.cfg_handler.config['server']['port']}.")
	with open('./keys/server.pem') as f:
		certData = f.read()
	certificate = ssl.PrivateCertificate.loadPEM(certData).options()
	# openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.crt
	reactor.listenSSL(core.cfg_handler.config["server"]["port"], factory, certificate)
	logging.info("Running the reactor.")
	reactor.run()

if __name__ == '__main__':
	main()