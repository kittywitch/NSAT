#!/usr/bin/env python

# external
from twisted.internet import ssl, reactor
import logging, os, threading, coloredlogs
# internal
import core, server

def main():
	threading.current_thread().name = 'NSATServer'
	# Sets up a debug level logger that overwrites the file
	logging.basicConfig(level=logging.DEBUG,filemode="w")
	logFormatter = logging.Formatter("[%(asctime)s - %(levelname)s] [%(filename)s:%(lineno)s - %(funcName)s() - %(threadName)s] %(message)s", "%Y-%m-%d %H:%M:%S")
	rootLogger = logging.getLogger()
	# Remove the default logger.
	rootLogger.handlers = []
	# Hook the logger up to the file "server.log"
	fileHandler = logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath( __file__ )), "server.log"))
	fileHandler.setFormatter(logFormatter)
	rootLogger.addHandler(fileHandler)
	# Hook the logger up to the console
	coloredlogs.install(level='DEBUG',fmt="[%(asctime)s - %(levelname)s] [%(filename)s:%(lineno)s - %(funcName)s() - %(threadName)s] %(message)s")

	print("""                                    

888888ba  .d88888b   .d888888  d888888P 
88    `8b 88.    "' d8'    88     88    
88     88 `Y88888b. 88aaaaa88a    88    
88     88       `8b 88     88     88    
88     88 d8'   .8P 88     88     88    
dP     dP  Y88888P  88     88     dP        
		                   
A python3 network service analytics tool - server section.
""")

	# Shared variables between files.
	core.init()

	# Automatically loads all .py files as modules from ./modules.
	core.import_dir(os.path.join(os.path.dirname(os.path.abspath( __file__ )), "modules"))

	factory = server.NSTServerFactory()
	with open(os.path.join(os.path.dirname(os.path.abspath( __file__ )), "keys/server.pem")) as f:
		certData = f.read()
	certificate = ssl.PrivateCertificate.loadPEM(certData).options()
	# openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
	logging.info(f"Binding reactor to port {core.config.server.port}.")
	reactor.listenSSL(core.config.server.port, factory, certificate)
	logging.info("Running the reactor.")
	reactor.run()

if __name__ == '__main__':
	main()