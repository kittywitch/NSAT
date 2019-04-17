import json
import mod

class protocolHandler():
	def __init__(self, err_handler, cfg_handler):
		self.err_handler = err_handler
		self.cfg_handler = cfg_handler
		print("[ProtocolHandler] Intialised.")

	def on_connect(self, server):
		pass

	def handle_line(self, line, server):
		# Push the JSON to the JSON validator, which returns the decoded JSON if it doesn't fail, otherwise kills the server
		json_line = self.validate_json(line, server)
		if json_line:
			action = self.validate_action(json_line, server)
			if action:
				data = self.validate_data(json_line)
				if data:
					self.execute_action(action, data, server)
				else:
					return
			else:
				return
		else:
			return

	# Parses the JSON and turns it into usable data structures, failing that, errors.
	def validate_json(self, line, server):
		# Messages from here will be marked "ValidateJSON".
		try:
			json_line = json.loads(line)
			if self.cfg_handler.config["server"]["debug"]:
				print("[ValidateJSON-Debug] %s" % json_line)
			return json_line
		except ValueError as e:
			print("[ValidateJSON] \"%s\" is not valid JSON." % line)
			self.err_handler.handle_error("ValidateJSON", e, server)
			return

	# Checks if there was an action in the JSON, if there was, checks if it's in the function DB, failing that, errors.
	def validate_action(self, line, server):
		# Messages from here will be marked "ValidateAction".
		if "action" in line:
			if line["action"] in mod.mod_db:
				if self.cfg_handler.config["server"]["debug"]:
					print("[ValidateAction-Debug] Valid action \"%s\" provided." % line["action"])
				return mod.mod_db[line["action"]]
			else:
				self.err_handler.handle_error("ValidateAction", "Action \"%s\" does not exist." % line["action"], server)
				return
		else:
			self.err_handler.handle_error("ValidateAction", "No action was provided.", server)
			return

	# TODO: Data validation from patterns and input things.
	def validate_data(self, data):
		return data

	# Takes the function from the module DB and executes it with the data provided, passing the server over to the function as a parameter too.
	def execute_action(self, action, data, server):
		print("[ExecuteAction] Executing \"%s\" with data: \"%s\"." % (action, data))
		action(data, server)
		pass