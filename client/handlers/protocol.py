import json, core, logging, uuid

class protocolHandler():
	def __init__(self):
		logging.info("Initialised.")

	def on_connect(self, client):
		# check if token exists, load it
		token = core.load_token()
		# registration process
		if token == None:
			# creates the same UUID every time
			r_id = str(uuid.uuid1(uuid.getnode()))
			# generate the token
			token = core.gen_token(r_id)
			# sends it to the server
			core.socket_send(client, "{\"action\":\"register\", \"uuid\":\"%s\", \"token\":\"%s\"}" % (r_id, token))
		else:
			r_id = uuid.uuid1(uuid.getnode())
			core.socket_send(client, "{\"action\":\"register\", \"uuid\":\"%s\", \"token\":\"%s\"}" % (r_id, token))

	def handle_line(self, line, client):
		# Push the JSON to the JSON validator, which returns the decoded JSON if it doesn't fail, otherwise kills the client
		json_line = self.validate_json(line, client)
		if json_line:
			action = self.validate_action(json_line, client)
			if action:
				data = self.validate_data(json_line)
				if data:
					self.execute_action(action, data, client)
				else:
					return
			else:
				return
		else:
			return

	# Parses the JSON and turns it into usable data structures, failing that, errors.
	def validate_json(self, line, client):
		# Messages from here will be marked "ValidateJSON".
		try:
			json_line = json.loads(line)
			if core.cfg_handler.config["client"]["debug"]:
				logging.debug(f"JSON output: {json_line}")
			return json_line
		except ValueError as e:
			logging.error(f"{line} is not valid JSON.")
			logging.error(f"{e}")
			return

	# Checks if there was an action in the JSON, if there was, checks if it's in the function DB, failing that, errors.
	def validate_action(self, line, client):
		# Messages from here will be marked "ValidateAction".
		if "action" in line:
			if line["action"] in core.mod_db:
				if core.cfg_handler.config["client"]["debug"]:
					logging.debug(f"Valid JSON action {line['action']} provided.")
				return core.mod_db[line["action"]]
			else:
				logging.error(f"JSON action \"{line['action']}\" does not exist.")
				return
		else:
			logging.error("No JSON action was provided.")
			return

	# TODO: Data validation from patterns and input things.
	def validate_data(self, data):
		return data

	# Takes the function from the coreule DB and executes it with the data provided, passing the client over to the function as a parameter too.
	def execute_action(self, action, data, client):
		logging.info(f"Executing \"{action}\" with \"{data}\".")
		action(data, client)
		pass