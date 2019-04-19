import json

class configHandler():
	def __init__(self):
		self.config = None
		print("[ConfigHandler] Intialised.")

	def load_config(self):
		# This is primarily for loading a JSON file into a variable for config purposes.
		print("[ConfigHandler] Loading config from \"./config.json\".")
		try:
			with open("config.json") as config_file:
				self.config = json.load(config_file)
			if self.config["server"]["debug"]:
				print("[ConfigHandler-Debug] Debug is enabled. Messages produced as a result of debug will have that suffixed to their system name.")
				print("[ConfigHandler-Debug] Contents of config: \"%s\"." % self.config)
			print("[ConfigHandler] Loaded config.")
		except:
			print("[ConfigHandler] Could not load \"./config.json\".")