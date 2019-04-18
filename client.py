from twisted.internet import ssl, reactor, endpoints, defer, task
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver
import uuid, json, os, hashlib, time

def load_token():
	if os.path.isfile(".token"):
		token_file = open(".token", "r")
		token = token_file.read()
		return token
	else:
		return None

def gen_token(id_in):
	# Generates a token from a given UUID by salting it with the current time and a unique UUID and SHA512 hashing it, returns the result.
	rand_uuid = str(uuid.uuid4())
	time_now = time.time()
	result = "%s%s%s" % (id_in, time_now, rand_uuid)
	print(result)
	return hashlib.sha512(result.encode("utf-8")).hexdigest()

def store_token(token):
	return token

def socket_send(client, data):
	client.sendLine(data.encode("utf-8"))

class NSTClient(LineReceiver):
	def connectionMade(self):
		# check if token exists, load it
		token = load_token()
		# registration process
		if token == None:
			# creates the same UUID every time
			r_id = str(uuid.uuid1(uuid.getnode()))
			# generate the token
			token = gen_token(r_id)
			# sends it to the server
			socket_send(self, "\"action\":\"register\", \"uuid\":\"%s\", \"token\":\"%s\"}" % (r_id, token))
		else:
			r_id = uuid.uuid1(uuid.getnode())
			socket_send(self, "{\"action\":\"register\", \"uuid\":\"%s\", \"token\":\"%s\"}" % (r_id, token))

	def lineReceived(self, line):
		jsonLine = json.loads(line)
		# server tells the client to store the token
		if jsonLine["action"] == "enroll_token" and load_token() == None:
			token_file = open(".token", "w+")
			token = jsonLine["token"]
			token_file.write(token)
			print("Registered token from server. Token: \"%s\"." % token)
			token_file.close()


class NSTClientFactory(ClientFactory):
    protocol = NSTClient

    def clientConnectionFailed(self, connector, reason):
        print("connection failed: ", reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("connection lost: ", reason.getErrorMessage())
        reactor.stop()

def main():
	factory = NSTClientFactory()
	reactor.connectSSL('127.0.0.1', 50000, factory, ssl.CertificateOptions(verify=False))
	reactor.run()

if __name__ == '__main__':
	main()