# external
import logging, time, hashlib, json, os, threading, re, imp, inspect, yaml
# internal
import handlers.sms, handlers.pushover

# - - - - - - - - - - - - - 
# Directory Modules Loader
# - - - - - - - - - - - - -

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

# - - - - - - - - - - - - - 
# Token System 
# TODO: redo this
# - - - - - - - - - - - - -

# adds a token to the database and the token database file.
# does the token DB file exist, if not, create it
def add_token(uuid, token):
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

# - - - - - - - - - - - - - 
# Modular Action System 
# - - - - - - - - - - - - -

# this is used as a decorator within the modules/ folders.
# it adds a key value pair to actions, where the key => the name of the action, value => the function that corresponds to it
# example:
# @core.add_action("hello_world")
# def hello_world(data, server):
#   pass
def add_action(name):
	frame = inspect.stack()[1]
	filename = os.path.relpath(frame[0].f_code.co_filename, ex_dir)
	def wrapper(function):
		actions[name] = function
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
		logging.info(f"Loaded timer for \"{function}\" that runs every {time} seconds from \"{filename}\".")
		return function
	return wrapper

# takes an action name, returns the corresponding function from actions
def get_action(name):
	# checks that input is provided to the function
	if name is not None or name is not "":
		# checks if the input is a key within the actions database
		if name in actions:
			# takes the action, which is the actual function that is the value corresponding to that key.
			action = actions[name]
			if config.server.debug:
				logging.debug(f"Valid action \"{name}\" provided, corresponds to the action \"{action}\".")
			return action
		else:
			return ValueError("Action provided does not exist within the action database.")
	else:
		return ValueError("No action provided.")

# - - - - - - - - - - - - - 
# Config System 
# - - - - - - - - - - - - -

# makes a dict usable as an object
class DictToObj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [DictToObj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, DictToObj(b) if isinstance(b, dict) else b)

# this loads a YAML file into core.config as an object
def load_config():
	logging.info("Loading config from \"./config.yaml\".")
	try:
		with open(os.path.join(ex_dir, "config.yaml")) as config_file:
			config = DictToObj(yaml.load(config_file.read(), Loader=yaml.FullLoader))
			logging.info("Loaded config.")
			return config
		if config.server.debug:
			logging.debug("Debug is enabled.")
			logging.debug(f"Config contains \"{config}\".")
	except:
		logging.critical("Could not load \"./config.yaml\".")

# - - - - - - - - - - - - - 
# Helpers
# - - - - - - - - - - - - -

# provides an easy function for encoding data without being inline with other things, such as % style replacements.
def socket_send(server, data):
	server.sendLine(data.encode("utf-8"))

# - - - - - - - - - - - - - 
# Sets everything up
# - - - - - - - - - - - - -

def init():
	# server list, stores NSTServer objects
	global servers
	servers = []
	# executable directory, the directory this file is within
	global ex_dir
	ex_dir = os.path.dirname(os.path.abspath( __file__ ))
	# actions database, key => action string, value => function
	global actions
	actions = {}
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
	global config
	config = load_config()
	# initialised after due to requiring the config
	global capabilities
	capabilities = {
		"sms":handlers.sms.init(),
		"pushover":handlers.pushover.init()
	}