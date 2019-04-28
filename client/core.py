# external
import logging, time, hashlib, json, os, uuid, re, imp, inspect, yaml

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

# loads the token from the json file
def load_token():
	if os.path.isfile(os.path.join(ex_dir, ".token")):
		token_file = open(os.path.join(ex_dir, ".token"), "r")
		token_opts = json.loads(token_file.read())
		logging.info(f"Loaded {token_opts}")
		return (token_opts["uuid"], token_opts["token"])
	else:
		return (None, None)

# generates a token to be used for the server
def gen_token(id_in):
	# Generates a token from a given UUID by salting it with the current time and a unique UUID and SHA512 hashing it, returns the result.
	rand_uuid = str(uuid.uuid4())
	time_now = time.time()
	result = "%s%s%s" % (id_in, time_now, rand_uuid)
	logging.info(f"Generated token: {result}")
	return hashlib.sha512(result.encode("utf-8")).hexdigest()

def store_token(token):
	return token

# - - - - - - - - - - - - - 
# Modular Action System 
# - - - - - - - - - - - - -

# this is used as a decorator within the modules/ folders.
# it adds a key value pair to actions, where the key => the name of the action, value => the function that corresponds to it
# example:
# @core.add_action("hello_world")
# def hello_world(data, client):
#   pass
def add_action(name):
	frame = inspect.stack()[1]
	filename = os.path.relpath(frame[0].f_code.co_filename, ex_dir)
	def wrapper(function):
		actions[name] = function
		logging.info(f"Loaded function \"{function}\" as \"{name}\" from \"{filename}\".")
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
			if config.client.debug:
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
		if config.client.debug:
			logging.debug("Debug is enabled.")
			logging.debug(f"Config contains \"{config}\".")
	except:
		logging.critical("Could not load \"./config.yaml\".")

# - - - - - - - - - - - - - 
# Helpers
# - - - - - - - - - - - - -

# provides an easy function for encoding data without being inline with other things, such as % style replacements.
def socket_send(client, data):
	client.sendLine(data.encode("utf-8"))

# - - - - - - - - - - - - - 
# Sets everything up
# - - - - - - - - - - - - -

def init():
	global client
	global ex_dir
	ex_dir = os.path.dirname(os.path.abspath( __file__ ))
	# Modules Database, key => action, value => function
	global actions
	actions = {}
	# initialises core.config
	global config
	config = load_config()
	# loads token from file for reestablish
	global uid
	global token
	uid, token = load_token()