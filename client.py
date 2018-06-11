import sys
import socket

class Client(object):
    
    def __init__(self, ip, port, extra):
        self.State = "Conectat"
        self.error = ""
        self.ip = ip
        self.port = port
        self.connect_to_server()
        self.init_extra(extra)

    def connect_to_server(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        try:
            self.server = self.client.connect((self.ip, self.port))
        except ConnectionRefusedError as e:
            self.State = "No conectat"
            self.error = str(e)
        

    def disconnect_from_server(self):
        self.client.close()
    def init_extra (self, extra):
        return
    def recieve_message(self):
        msg = self.client.recv(4096)
        self.disconnect_from_server()
    def send_message(self, message):
        self.connect_to_server()
        if (isinstance(message, str)):
            message = message.encode(encoding="utf-8")
        try:
            self.client.sendall(message)
        except Exception as e:
            self.error = str(e)
        self.recieve_message()
            
    def close_server(self):
        self.client.close()
    __recieve_message = recieve_message
    __send_message = send_message
    __close_server = close_server
