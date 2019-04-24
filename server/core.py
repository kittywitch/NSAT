import logging, time, hashlib, handlers.config, handlers.protocol, handlers.sms, handlers.po, json, os

def init():
	# Modules Database, key => action, value => function
	global mod_db
	mod_db = {}
	# Tokens database, backends to a file.
	global token_db
	if os.path.isfile(".token_db"):
		token_file = open(".token_db", "r+")
		token_db = json.loads(token_file.read())
		logging.info("Token DB opened.")
		token_file.close()
	else:
		token_db = {}
	# Handlers
	global cfg_handler
	cfg_handler = handlers.config.configHandler()
	cfg_handler.load_config()
	# sms handler requires config handler initialised
	handlers.sms.init()
	global notify_sms
	notify_sms = handlers.sms.notify_sms
	global notify_call
	notify_call = handlers.sms.notify_call
	handlers.po.init()
	global notify_po
	notify_po = handlers.po.notify_po
	global proto_handler
	proto_handler = handlers.protocol.protocolHandler()

# Provides an easy function for encoding data without being inline with other things, such as % style replacements.
def socket_send(server, data):
	server.sendLine(data.encode("utf-8"))

# This implements the ModuleHandler, this uses decorators, so this is accessed by @core.add_action(name) before a function definition for a module.
def add_action(name):
	def wrapper(function):
		mod_db[name] = function
		logging.info("Loaded function \"%s\"." % name)
		return function
	return wrapper

def add_token(uuid, token):
	# Adds a token to the database and the token database file.
	# does the token DB file exist, if not, create it
	if os.path.isfile(".token_db"):
		token_db[uuid] = token
		# read it, import the JSON data structures
		token_file = open(".token_db", "r+")
		token_obj = json.loads(token_file.read())
		# add the token
		token_obj[uuid] = token
		# overwrite the file
		token_file.seek(0)
		token_file.write(json.dumps(token_obj))
		token_file.close()
		logging.info("Added token for \"%s\"." % uuid)
	else:
		token_db[uuid] = token
		# read it, import the JSON data structures
		token_file = open(".token_db", "w+")
		token_file.write(json.dumps(token_db))
		logging.info("Added token for \"%s\"." % uuid)