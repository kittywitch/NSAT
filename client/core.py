import logging, time, hashlib, handlers.config, handlers.protocol, json, os

# Provides an easy function for encoding data without being inline with other things, such as % style replacements.
def socket_send(client, data):
	client.sendLine(data.encode("utf-8"))

def load_token():
	if os.path.isfile(".token"):
		token_file = open(".token", "r")
		token = token_file.read()
		return token
	else:
		return None

def gen_token(id_in):
	# Generates a token from a given UUID by salting it with the current time and a unique UUID and SHA512 hashing it, returns the result.
	rand_uuid = str(uuid.uuid4())
	time_now = time.time()
	result = "%s%s%s" % (id_in, time_now, rand_uuid)
	print(result)
	return hashlib.sha512(result.encode("utf-8")).hexdigest()

def store_token(token):
	return token
	
# This implements the ModuleHandler, this uses decorators, so this is accessed by @core.add_action(name) before a function definition for a module.
def add_action(name):
	def wrapper(function):
		mod_db[name] = function
		logging.info("Loaded function \"%s\"." % name)
		return function
	return wrapper

def init():
	# Modules Database, key => action, value => function
	global mod_db
	mod_db = {}
	# Handlers
	global cfg_handler
	cfg_handler = handlers.config.configHandler()
	cfg_handler.load_config()

	global proto_handler
	proto_handler = handlers.protocol.protocolHandler()