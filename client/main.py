#!/usr/bin/env python

# external
from twisted.internet import ssl, reactor, endpoints, defer, task
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver
import uuid, json, os, hashlib, time, logging
# internal
import core, client

def main():
	# Sets up a debug level logger that overwrites the file
	logging.basicConfig(level=logging.DEBUG,filemode="w")
	# fancy: [2019-04-26 12:38:53,919 - INFO] [core.py:37 - init() - MainThread] Token DB opened.
	logFormatter = logging.Formatter('[%(asctime)s - %(levelname)s] [%(filename)s:%(lineno)s - %(funcName)s() - %(threadName)s] %(message)s')
	rootLogger = logging.getLogger()
	# Remove the default logger.
	rootLogger.handlers = []
	# Hook the logger up to the file "server.log"
	fileHandler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath( __file__ )), "client.log"))
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
	
	factory = client.NSTClientFactory()
	security_form = "with certificate verification" if core.config.client.tls_verify else "without certificate verification"
	logging.info(f"Connecting reactor to port {core.config.client.address}:{core.config.client.port} {security_form}.")
	reactor.connectSSL(core.config.client.address, core.config.client.port, factory, ssl.CertificateOptions(verify=core.config.client.tls_verify))
	logging.info("Running the reactor.")
	reactor.run()

if __name__ == '__main__':
	main()