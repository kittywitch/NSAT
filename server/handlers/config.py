import logging, os, core, yaml

class configHandler():
	def __init__(self):
		pass

	def load_config(self):
		# This is primarily for loading a JSON file into a variable for config purposes.
		logging.info("Loading config from \"./config.yaml\".")
		try:
			with open(os.path.join(core.ex_dir, "config.yaml")) as config_file:
				core.config = yaml.load(config_file.read(), Loader=yaml.FullLoader)
			if core.config["server"]["debug"]:
				logging.debug("Debug is enabled.")
				logging.debug("Contents of config: \"%s\"." % core.config)
			logging.info("Loaded config.")
		except:
			logging.critical("Could not load \"./config.yaml\".")