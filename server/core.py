import time, hashlib, handlers, json, os, twilio_handler

def init():
	# Modules Database, key => action, value => function
	global mod_db
	mod_db = {}
	# Tokens database, backends to a file.
	global token_db
	token_db = {}
	# Handlers
	global err_handler
	err_handler = handlers.error.errorHandler()
	global cfg_handler
	cfg_handler = handlers.config.configHandler()
	global proto_handler
	proto_handler = handlers.protocol.protocolHandler()

def socket_send(server, data):
	server.sendLine(data.encode("utf-8"))

def add_action(name):
	def wrapper(function):
		mod_db[name] = function
		print("[ModuleHandler] Loaded function \"%s\"." % name)
		return function
	return wrapper

def add_token(uuid, token):
	# Adds a token to the database and the token database file.
	# does the token DB file exist, if not, create it
	if os.path.isfile(".token_file"):
		token_db[uuid] = token
		# read it, import the JSON data structures
		token_file = open(".token_db", "r+")
		tokens_obj = json.loads(token_file)
		# add the token
		token_obj[uuid] = token
		# overwrite the file
		token_file.seek(0)
		token_file.write(json.dumps(token_obj))
		token_file.close()
		print("[TokenDB] Added token for %s." % uuid)
	else:
		token_db[uuid] = token
		# read it, import the JSON data structures
		token_file = open(".token_db", "w+")
		token_file.write(json.dumps(token_db))
		print("[TokenDB] Added token for %s." % uuid)