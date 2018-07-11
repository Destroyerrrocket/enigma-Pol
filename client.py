import sys
import socket
from bash import Bash
import json
class Client(object):
    
    def __init__(self, ip, port, bash = Bash(),extra = []):
        self.State = "Conectat"
        self.error = ""
        self.lastsent = ""
        self.ip = ip
        self.port = port
        self.bash = bash
        
        self.actions = []
        self.id = 0

        self.people = []
        self.connect_to_server()
        self.init_extra(extra)
        self.checkstatus()

    def init_extra(self, extra):
        return

    def print_data(self, message=""):
        return

    def disconnect_from_server(self):
        self.client.close()
    
    def connect_to_server(self):
        self.client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.client.settimeout(100)
        try:
            self.server = self.client.connect((self.ip, self.port))
        except ConnectionRefusedError as e:
            self.State = "No conectat"
            self.error = str(e)

    def recieve_message(self):
        msg = self.client.recv(4096)
        unbitedmsg = ""
        if msg.decode(encoding="utf-8") is not '':
            self.error = ""
            unbitedmsg = json.loads(msg.decode())
        elif self.error is not "":
            unbitedmsg = {"type": "error", "message": self.lastsent}
        if unbitedmsg is '':
            unbitedmsg = {"type": "error", "message": "Server seems like it failed. Unexpected action?"}
        return unbitedmsg

    def process_data(self, message):
        previous_last_entry = len(self.actions)
        for answer_entry in message["all"]:
            self.actions.append(answer_entry)
        self.print_data(message=str(json.dumps(message, indent=4)))
        for action in self.actions:
            if action["type"] == "personadd":
                if (action["name"] in self.people) != True:
                    self.people.append(action["name"])

            elif action["type"] == "personremove":
                for i in range(0, self.people):
                    if self.people[i] == action["name"]:
                        self.people.pop(i)
                self.people.pop(0)
        
    def send_message(self, message="", type_message="message", to="", extra={}):
        if type_message == "message":  
            self.lastsent = message
        
        our_data = {
            "type"              : type_message,
            "message"           : message,
            "id"                : self.id,
            "name"              : self.bash.current_name(),
            "to"                : "all",
            "client_action_size": len(self.actions)
        }
        arrextra = self.bash.dict_to_array(extra)
        for ext in arrextra:
            our_data[ext[0]] = ext[1]
        
        bited_our_data = json.dumps(our_data, indent=4).encode()

        self.connect_to_server()
        try:
            self.client.sendall(bited_our_data)
        except Exception as e:
            self.error = str(e)


    def checkstatus(self):
        if (self.State != "Conectat"):
            self.print_data(self.error)
        elif self.actions == []:
            self.first_connection()
        self.disconnect_from_server()

    def first_connection(self):
        self.ask_for_id()

        self.send_message(type_message="personadd")
        answer = self.recieve_message()
        self.process_data(answer)
        

        
    def ask_for_id(self):
        self.send_message(type_message="get_id_from_pool")
        answer = self.recieve_message()
        self.id = answer["all"][0]["message"]

"""     __recieve_message = recieve_message
    __send_message = send_message
    __close_server = close_server
    __disconnect_from_server = disconnect_from_server
 """
