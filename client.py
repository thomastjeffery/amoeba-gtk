import zmq
import msgpack

class Client():
    def __init__(self, server="tcp://localhost:5555"):
        self.context = zmq.Context()

        # Connect to server
        print("Connecting to \"%s\"..." % server)
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(server)

    def get_reply(self):
        # Get reply
        reply = msgpack.unpackb(self.socket.recv())
        return reply

    def request(self, request):
        # Send request
        self.socket.send(msgpack.packb(request))

if __name__ == "__main__":
    client = Client()

    for iteration in range(1, 6):
        request = {
            "quit": False,
            "buffer.insert": ("Request: %s\n" % iteration, 0),
            "buffer.print": "Request: %s" % iteration
        }
        if iteration == 5:
            request["quit"] = True

        try:
            # Send request
            print("Sending request %s..." % iteration)
            client.request(request)
        except KeyboardInterrupt:
            print("\nRecieved keyboard interrupt. Shutting down...")
            break

        try:
            # Recieve reply
            print("Recieved reply: %s" % client.get_reply().decode("UTF-8"))
        except KeyboardInterrupt:
            print("\nRecieved keyboard interrupt. Shutting down...")
            break
