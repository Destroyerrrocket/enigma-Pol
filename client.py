import sys
import socket
import custom_socket
from threading import Thread
import json
from bash import Bash

class Client(object):

    def __init__(self, ip, port, bash = Bash(),extra = []):
        self.State = "Conectat"
        self.error = ""
        self.lastsent = ""
        self.ip = ip
        self.port = port
        self.bash = bash

        self.actions = []
        self.server_fp = ""
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
        self.client = custom_socket.c_socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.client.settimeout(100)
        try:
            self.server = self.client.connect((self.ip, self.port))
        except ConnectionRefusedError as e:
            self.State = "No conectat"
            self.error = str(e)

    def recieve_message(self):
        msg = self.client.recvall()
        unbitedmsg = ""
        if msg.decode(encoding="utf-8") is not '':
            try:
                deencrypted = self.bash.decrypt_message(msg.decode())
                jsoning = deencrypted.data.decode()
                unbitedmsg = json.loads(jsoning)
            except:
                unbitedmsg = json.loads(msg.decode())
        elif self.error != "":
            unbitedmsg = {}
            unbitedmsg["all"] = []
            unbitedmsg["all"].append({"type": "error", "message": self.error})
        if unbitedmsg is '':
            unbitedmsg = {}
            unbitedmsg["all"] = []
            unbitedmsg["all"].append({"type": "error", "message": "Server seems like it failed. Unexpected action? error: " + self.error})
        return unbitedmsg

    def process_incoming_data(self, message):
        #previous_last_entry = len(self.actions)
        for answer_entry in message["all"]:
            self.actions.append(answer_entry)
            if answer_entry["type"] == "personadd":
                if (answer_entry["name"] not in self.people):
                    self.people.append(answer_entry["name"])
            elif answer_entry["type"] == "personremove":
                for i in range(0, self.people):
                    if self.people[i] == answer_entry["name"]:
                        self.people.pop(i)
                self.people.pop(0)
            elif answer_entry["type"] == "message":
                self.print_data("[" + answer_entry["name"] + "]: " + answer_entry["message"])
            elif answer_entry["type"] == "server_key":
                self.bash.import_key(answer_entry["message"])
                self.server_fp = answer_entry["fp"]
            elif answer_entry["type"] == "error":
                self.print_data("[ERROR]: " + answer_entry["message"])
        # line for debugging
        # self.print_data(message=str(json.dumps(message, indent=4)))


    def send_message(self, message="", type_message="message", to="", extra={}):
        if type_message == "message":
            self.lastsent = message

        our_data = {
            "type"              : type_message,
            "message"           : message,
            "id"                : self.id,
            "name"              : self.bash.current_name(),
            "to"                : "all",
            "client_action_size": len(self.actions),
            "fp"                : self.bash.load_data("personal private key")
        }
        arrextra = self.bash.dict_to_array(extra)
        for ext in arrextra:
            our_data[ext[0]] = ext[1]
        if self.server_fp != "":
            bited_our_data = str(self.bash.encrypt_message(json.dumps(our_data, indent=4), self.server_fp)).encode()
        else:
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
        self.get_actions()
        self.ask_for_id()
        our_public_key = self.bash.export_key(self.bash.load_data("personal private key"))
        self.send_message(message=our_public_key, type_message="personadd")
        answer = self.recieve_message()
        self.process_incoming_data(answer)

    def get_actions(self):
        self.send_message(type_message="get_actions")
        answer = self.recieve_message()
        self.process_incoming_data(answer)

    def ask_for_id(self):
        self.send_message(type_message="get_id_from_pool")
        answer = self.recieve_message()
        self.id = answer["all"][0]["message"]

"""     __recieve_message = recieve_message
    __send_message = send_message
    __close_server = close_server
    __disconnect_from_server = disconnect_from_server
 """
