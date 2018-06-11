import sys
import socket

class Client(object):
    
    def __init__(self, ip, port, extra):
        self.State = "Conectat"
        self.error = ""
        self.ip = ip
        self.port = port
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        try:
            self.server = self.client.connect((self.ip, self.port))
        except ConnectionRefusedError:
            self.State = "No conectat"
            self.error = "Error: no connection to server"
        self.init_extra(extra)
    def init_extra (self, extra):
        return
    def recieve_message(self):
        msg = self.client.recv(4096)
    def send_message(self, message):
            self.client.sendall(message)
            
    def close_server(self):
        self.client.close()
    __recieve_message = recieve_message
    __send_message = send_message
    __close_server = close_server
