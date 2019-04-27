# external
from twisted.internet import endpoints, defer, task, reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver
import logging, json, uuid
# internal
import core

# unserialises the JSON recieved
def deserialise(line, client):
        try:
            data = json.loads(line)
            if core.config.client.debug:
                logging.debug(f"Received \"{data}\" from server.")
            return data
        except Exception as e:
            logging.error(f"Line \"{line}\" received from server is not valid JSON.")
            logging.error(f"Error: \"{e}\".")
            return e

class NSTClient(LineReceiver):
    def connectionMade(self):
        if core.token == None or core.uid == None:
            # creates the same UUID every time
            r_id = str(uuid.uuid1(uuid.getnode()))
            # generate the token
            token = core.gen_token(r_id)
            # sends it to the server
            core.socket_send(self, json.dumps({
                "action":"register",
                "uuid":r_id,
                "token":token
            }))
        else:
            r_id = uuid.uuid1(uuid.getnode())
            core.socket_send(self, json.dumps({
                "action":"reestablish",
                "uuid":core.uid,
                "token":core.token
            }))

    def lineReceived(self, line):
        # takes the JSON and turns it into a python dict OR returns the error
        unsafe_data = deserialise(line, self)
        # checking if the type returned is a dictionary and not an exception
        if isinstance(unsafe_data, dict):
            data = unsafe_data
        else:
            return
        # action checking
        unsafe_action = core.get_action(data["action"])
        if callable(unsafe_action):
            action = unsafe_action
            action(data, self)
        else:
            return


class NSTClientFactory(ClientFactory):
    protocol = NSTClient

    def clientConnectionFailed(self, connector, reason):
        logging.error(f"Connection failed {reason.getErrorMessage()}")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        logging.error(f"Connection lost: {reason.getErrorMessage()}")
        reactor.stop()