import time
import datetime
import socket
import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 1234
    buf = 1024
    print("press Ctrl+C to stop the server")
    try:
        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((host, port), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            print("running on " + str(server.server_address))
            server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.shutdown()
        