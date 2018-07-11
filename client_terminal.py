import threading
from client import Client

class Client_terminal(Client):
    def init_extra(self, extra):
        self.terminfo = [" "] *extra[1]
        self.refresh = 0

    def print_data(self, message="", type_message="message", extra={}):
        if type_message == "message":
            arraymessage = message.splitlines()
            for line in arraymessage:
                self.terminfo.append(line)
                self.terminfo.pop(0)
        self.checkstatus()
