import threading
import sys
from client import Client


class Client_terminal(Client):
    def init_extra(self, extra):
        self.terminfo = [" "] * extra[1]
        self.history = []
        self.his_pint_in_time = 0
        self.max_size = extra[1]
        self.refresh = 0

    def print_data(self, message="", type_message="message", extra={}):
        if type_message == "message":
            arraymessage = message.splitlines()
            for line in arraymessage:
                self.terminfo.clear()

                self.history.insert(0, line)
                for i in range(0, self.max_size):
                    try:
                        if (len(self.history) > i and len(self.history) != 0):
                            self.terminfo.insert(
                                0, self.history[i + self.his_pint_in_time])
                        else:
                            self.terminfo.insert(0, " ")
                    except IndexError:
                        sys.exit(str(len(self.history)))

    def up(self):
        if len(self.history) > +self.his_pint_in_time + self.max_size:
            self.his_pint_in_time += 1
        self.terminfo.clear()
        for i in range(0, self.max_size):
            try:
                if (len(self.history) > i and len(self.history) != 0):
                    self.terminfo.insert(
                        0, self.history[i + self.his_pint_in_time])
                else:
                    self.terminfo.insert(0, " ")
            except IndexError:
                sys.exit(
                    str(len(self.history)) + "<" +
                    str(self.his_pint_in_time + self.max_size))

    def down(self):
        if self.his_pint_in_time > 0:
            self.his_pint_in_time -= 1
        self.terminfo.clear()
        for i in range(0, self.max_size):
            try:
                if (len(self.history) > i and len(self.history) != 0):
                    self.terminfo.insert(
                        0, self.history[i + self.his_pint_in_time])
                else:
                    self.terminfo.insert(0, " ")
            except IndexError:
                sys.exit(
                    str(len(self.history)) + ">" + str(self.his_pint_in_time))
