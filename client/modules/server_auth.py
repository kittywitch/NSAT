import core, logging
@core.add_action("enroll_token")
def enroll_token(data, client):
	if core.load_token() == None:
		token_file = open(".token", "w+")
		token = jsonLine["token"]
		token_file.write(token)
		print("Registered token from server. Token: \"%s\"." % token)
		token_file.close()

@core.add_action("reject")
def reject(data, client):
	client.transport.loseConnection()