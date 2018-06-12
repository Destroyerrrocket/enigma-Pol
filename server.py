#!/bin/python3
import time
import datetime
import socket
import socketserver
from bash import Bash 

class MyTCPHandler(socketserver.BaseRequestHandler):
        
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        #self.data = str(self.data)
        print(self.data)
        self.Decide_what_to_do(self.data)
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
    def Decide_what_to_do(self, message):
        strmessage = message.decode(encoding="utf-8")
        if "/info_server" in strmessage:
            self.send_back("Last message id: " + str(lstmsgid) + "\nList of people: " + str(len(people)))
        else:
            self.send_back(message)

    def send_back(self, message):
        self.request.sendall(message)
if __name__ == "__main__":
    global bash, people, lstmsgid
    bash = Bash(".server_keypool")
    people = {}
    lstmsgid = 0
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
        
