# external
import logging, time, hashlib, json, os, uuid, re, imp, inspect
# internal
import handlers.config, handlers.protocol

# this function checks for files with ".py" in the directory, then adds them to a list
def modules_in_dir(path):
	result = set()
	for entry in os.listdir(path):
		if os.path.isfile(os.path.join(path, entry)):
			matches = re.search("(.+\.py)$", entry)
			if matches:
				result.add(matches.group(0))
	return result

# this function uses imp.load_module to load those files somewhat manually, but, providing a wildcard import for a dir
def import_dir(path):
	for filename in sorted(modules_in_dir(path)):
		search_path = os.path.join(os.getcwd(), path)
		module_name, ext = os.path.splitext(filename)
		fp, path_name, description = imp.find_module(module_name, [search_path,])
		module = imp.load_module(module_name, fp, path_name, description)

# Provides an easy function for encoding data without being inline with other things, such as % style replacements.
def socket_send(client, data):
	client.sendLine(data.encode("utf-8"))

def load_token():
	if os.path.isfile(os.path.join(ex_dir, ".token")):
		token_file = open(os.path.join(ex_dir, ".token"), "r")
		token_opts = json.loads(token_file.read())
		logging.info(f"Loaded {token_opts}")
		return (token_opts["uuid"], token_opts["token"])
	else:
		return (None, None)

def gen_token(id_in):
	# Generates a token from a given UUID by salting it with the current time and a unique UUID and SHA512 hashing it, returns the result.
	rand_uuid = str(uuid.uuid4())
	time_now = time.time()
	result = "%s%s%s" % (id_in, time_now, rand_uuid)
	logging.info(f"Generated token: {result}")
	return hashlib.sha512(result.encode("utf-8")).hexdigest()

def store_token(token):
	return token
	
# This implements the ModuleHandler, this uses decorators, so this is accessed by @core.add_action(name) before a function definition for a module.
def add_action(name):
	frame = inspect.stack()[1]
	filename = os.path.relpath(frame[0].f_code.co_filename, ex_dir)
	def wrapper(function):
		mod_db[name] = function
		logging.info(f"Loaded function \"{function}\" as \"{name}\" from \"{filename}\".")
		return function
	return wrapper

def init():
	global ex_dir
	ex_dir = os.path.dirname(os.path.abspath( __file__ ))
	# Modules Database, key => action, value => function
	global mod_db
	mod_db = {}
	# initialises core.config
	cfg_handler = handlers.config.configHandler()
	cfg_handler.load_config()
	# loads token from file for reestablish
	global uid
	global token
	uid, token = load_token()
	# protocol handler
	global proto_handler
	proto_handler = handlers.protocol.protocolHandler()