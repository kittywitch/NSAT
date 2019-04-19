class errorHandler():
	def __init__(self):
		print("[ErrorHandler] Intialised.")

	# Messages from here will be marked "ErrorHandler".
	def handle_error(self, system, error, server):
		print("[ErrorHandler] Terminating connection due to error recieved from %s: \"%s\"." % (system, error))
		server.transport.abortConnection()