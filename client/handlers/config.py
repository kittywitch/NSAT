import json, logging

class configHandler():
	def __init__(self):
		self.config = None
		logging.info("Initialised.")

	def load_config(self):
		# This is primarily for loading a JSON file into a variable for config purposes.
		logging.info("Loading config from \"./config.json\".")
		try:
			with open("config.json") as config_file:
				self.config = json.load(config_file)
			if self.config["client"]["debug"]:
				logging.debug("Debug is enabled.")
				logging.debug("Contents of config: \"%s\"." % self.config)
			logging.info("Loaded config.")
		except:
			logging.critical("Could not load \"./config.json\".")