# external
import logging, time, hashlib, json, os, schedule, threading, re, imp, inspect
# internal
import handlers.config, handlers.protocol, handlers.sms, handlers.po

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

# provides an easy function for encoding data without being inline with other things, such as % style replacements.
def socket_send(server, data):
	server.sendLine(data.encode("utf-8"))

# this implements the ModuleHandler, this uses decorators, so this is accessed by @core.add_action(name) before a function definition for a module.
def add_action(name):
	frame = inspect.stack()[1]
	filename = os.path.relpath(frame[0].f_code.co_filename, ex_dir)
	def wrapper(function):
		mod_db[name] = function
		logging.info(f"Loaded function \"{function}\" as \"{name}\" from \"{filename}\".")
		return function
	return wrapper

# this starts the timer through decorators. TODO: make it so timers can be started and then repeatedly ran from core.py instead of within modules
def add_timer(time):
	frame = inspect.stack()[1]
	filename = os.path.relpath(frame[0].f_code.co_filename, ex_dir)
	def wrapper(function):
		first_timer = threading.Timer(time, function)
		first_timer.daemon = True
		first_timer.start()
		logging.info(f"Loaded timer for {function} that runs every {time} seconds from {filename}.")
		return function
	return wrapper

def add_token(uuid, token):
	# adds a token to the database and the token database file.
	# does the token DB file exist, if not, create it
	if os.path.isfile(os.path.join(ex_dir, ".token_db")):
		token_db[uuid] = token
		# read it, import the JSON data structures
		token_file = open(os.path.join(ex_dir, ".token_db"), "r+")
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
		token_file = open(os.path.join(ex_dir, ".token_db"), "w+")
		token_file.write(json.dumps(token_db))
		logging.info("Added token for \"%s\"." % uuid)

def determine_capacities():
	# checks if the keys exist in config["twilio"] required for twilio and checks that their value isn't None, i.e. empty
	if all(k in config["twilio"] for k in ["id", "token", "in", "out"]) and all(value is not None for value in config["twilio"].values()):
		capacities.append("sms")
	# checks if the keys exist in config["pushover"] required for pushover and checks that their value isn't None, i.e. empty
	if all(k in config["pushover"] for k in ["user", "token"]) and all(value is not None for value in config["pushover"].values()):
		capacities.append("pushover")
	logging.info(f"Registered {capacities}.")

def init():
	# shows what config capacities the server has
	global capacities
	capacities = []
	# server list, stores NSTServer objects
	global servers
	servers = []
	# executable directory, the directory this file is within
	global ex_dir
	ex_dir = os.path.dirname(os.path.abspath( __file__ ))
	# modules database, key => action, value => function
	global mod_db
	mod_db = {}
	# tokens database, backends to a file.
	global token_db
	if os.path.isfile(os.path.join(ex_dir, ".token_db")):
		token_file = open(os.path.join(ex_dir, ".token_db"), "r+")
		token_db = json.loads(token_file.read())
		logging.info("Token DB opened.")
		token_file.close()
	else:
		token_db = {}
	# initialises the value of core.config
	cfg_handler = handlers.config.configHandler()
	cfg_handler.load_config()
	# sms and po handlers require core.config
	handlers.sms.init()
	global notify_sms
	notify_sms = handlers.sms.notify_sms
	global notify_call
	notify_call = handlers.sms.notify_call
	handlers.po.init()
	global notify_po
	notify_po = handlers.po.notify_po
	# protocol implementation, layer above NSTServer
	global proto_handler
	proto_handler = handlers.protocol.protocolHandler()
	determine_capacities()