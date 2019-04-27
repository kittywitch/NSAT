#!/usr/bin/env python

# external
from twisted.internet import ssl, reactor
import logging, os
# internal
import core, server

def main():
	# Sets up a debug level logger that overwrites the file
	logging.basicConfig(level=logging.DEBUG,filemode="w")
	logFormatter = logging.Formatter('[%(asctime)s - %(levelname)s] [%(filename)s:%(lineno)s - %(funcName)s() - %(threadName)s] %(message)s')
	rootLogger = logging.getLogger()
	# Remove the default logger.
	rootLogger.handlers = []
	# Hook the logger up to the file "server.log"
	fileHandler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath( __file__ )), "server.log"))
	fileHandler.setFormatter(logFormatter)
	rootLogger.addHandler(fileHandler)
	# Hook the logger up to the console
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	rootLogger.addHandler(consoleHandler)

	# Shared variables between files.
	core.init()

	# Automatically loads all .py files as modules from ./modules.
	core.import_dir(os.path.join(os.path.dirname(os.path.abspath( __file__ )), "modules"))

	factory = server.NSTServerFactory()
	with open(os.path.join(os.path.dirname(os.path.abspath( __file__ )), "keys/server.pem")) as f:
		certData = f.read()
	certificate = ssl.PrivateCertificate.loadPEM(certData).options()
	# openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.crt
	logging.info(f"Binding reactor to port {core.config.server.port}.")
	reactor.listenSSL(core.config.server.port, factory, certificate)
	logging.info("Running the reactor.")
	reactor.run()

if __name__ == '__main__':
	main()