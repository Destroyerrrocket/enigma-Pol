import threading
from client import Client

class Client_terminal(Client):
    def init_extra(self, extra):
        self.terminfo = [" "] *extra[1]
        
        self.refresh = 0
        self.checkstatus()

    def recieve_message(self):
        try:
            msg = self.client.recv(4096)
            self.terminfo.append(msg)
            self.terminfo.pop(0)
            self.disconnect_from_server()
        except Exception as e:
            self.error = e
        self.checkstatus()
    def checkstatus(self):
        if (self.State != "Conectat"):
            self.terminfo.append(self.error)
            self.terminfo.pop(0)
        else:
            self.disconnect_from_server()
