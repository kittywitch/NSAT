import core, logging

@core.add_action("enroll_token")
def enroll_token(data, client):
	if core.load_token() == None:
		token_file = open(".token", "w+")
		token_file.write(f"{{\"token\":\"{data['token']}\", \"uuid\":\"{data['uuid']}\"}}")
		logging.info(f"Registered token from server. UUID: \"{data['uuid']}\", Token: \"{data['token']}\".")
		token_file.close()

@core.add_action("reject")
def reject(data, client):
	client.transport.loseConnection()

@core.add_action("authorised")
def on_authorisation(data, client):
	logging.info("Authorised for server.")