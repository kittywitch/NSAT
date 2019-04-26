import core, logging, json

@core.add_action("enroll_token")
def enroll_token(data, client):
	if core.uid == None or core.token == None:
		token_file = open(os.path.join(core.ex_dir, ".token"), "w+")
		core.uid = data['uuid']
		core.token = data['token']
		token_file.write(json.dumps({
			"token":data["token"],
			"uuid":data["uuid"]
		}))
		logging.info(f"Registered token from server. UUID: \"{data['uuid']}\", Token: \"{data['token']}\".")
		token_file.close()

@core.add_action("reject")
def reject(data, client):
	client.transport.loseConnection()

@core.add_action("authorised")
def on_authorisation(data, client):
	logging.info("Authorised for server.")