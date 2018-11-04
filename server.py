#!/usr/bin/env python3

global NAME_SERVER, PWD_SERVER, PORT, IP
NAME_SERVER = "polserver"
PWD_SERVER = "12345"
PORT = 12345
IP = "0.0.0.0"

import custom_socket
import socketserver
import os
import sys
import json
import random
from pprint import pprint # debug purposes
from bash import Bash

class MyTCPHandler(socketserver.BaseRequestHandler):


    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.recvall()
        #self.data = str(self.data)
        print("{} recv: ".format(self.client_address[0]) + self.data.decode())
        self.Decide_what_to_do(self.data)

    def Decide_what_to_do(self, bytedmessage):
        if bytedmessage != b'':
            try:
                deencrypted = bash.decrypt_message(bytedmessage.decode())
                message = json.loads(deencrypted.data.decode())
                # no imprimirem la informació sensitiva a la consola
                #print("decrypted: " + deencrypted.data.decode())
            except Exception as errorDecrypting:
                print("Not decrypting due to: " + str(errorDecrypting))
                message = json.loads(bytedmessage.decode())
            self.client_fp = message["fp"]
            if message["type"] == "get_id_from_pool":
                self.send_back_one(self.get_id_from_pool(), "id")
            elif message["type"] == "get_actions":
                if message["pwd"] == PWD_SERVER:
                    self.send_back_all(message["client_action_size"])
                else:
                    self.send_back_one(actions[0]["message"], actions[0]["type"])
            elif message["type"] == "personadd":
                if message["pwd"] == PWD_SERVER:
                    bash.import_key(message["message"])
                    message["message"] = "DELETED FOR SAFETY"
                    actions.append(message)
                    user_data = self.get_user_data(message)
                    self.send_back_all(message["client_action_size"], user_data=user_data)
                else:
                    message["message"] = "DELETED FOR SAFETY"
                    self.send_back_one("Contrasenya incorrecta", "message")
            elif message["type"] == "message":
                if message["pwd"] == PWD_SERVER:
                    actions.append(message)
                    user_data = self.get_user_data(message)
                    self.send_back_all(message["client_action_size"], user_data=user_data)
                else:
                    actions.append(message)
                    self.send_back_one("Has dit: " + message["message"])
            elif message["pwd"] == PWD_SERVER:
                actions.append(message)
                user_data = self.get_user_data(message)
                self.send_back_all(message["client_action_size"], user_data=user_data)
            else:
                pass

    def send_back_one(self, message="", type_message="message", extra = {}):
        encapsulated = {}
        encapsulated["all"] = []
        our_data = {
            "type": type_message,
            "message": message,
            "name": bash.current_name(),
            "to": "all",
            "fp": bash.load_data("personal private key")
        }
        our_data.update(extra)
        """ arrextra = bash.dict_to_array(extra)
        for ext in arrextra:
            our_data[ext[0]] = ext[1] """

        encapsulated["all"].append(our_data)
        if self.client_fp in bash.get_list_pukeys_fingerprint():
            not_yet_bited_our_data = str(bash.encrypt_message(json.dumps(encapsulated, indent=4), self.client_fp))
        else:
            not_yet_bited_our_data = json.dumps(encapsulated, indent=4)
        bited_our_data = not_yet_bited_our_data.encode()
        print("send: " + bited_our_data.decode())
        self.request.sendall(bited_our_data)


    def send_back_all(self, index=0, user_data={}):
        encapsulated = {}
        encapsulated["all"] = []
        # print("comencem a: " + str(index))

        for i in range(0, len(actions)):
            people = actions[i]["to"]
            #print(people)
            if i >= index:
                if people == "all" or people == user_data["id"]:
                    encapsulated["all"].append(actions[i])

            #if user_not_intended_to_see_this:
            #    encapsulated["all"].pop(i)

        if self.client_fp in bash.get_list_pukeys_fingerprint():
            not_yet_bited_our_data = str(bash.encrypt_message(json.dumps(encapsulated, indent=4), self.client_fp))
        else:
            not_yet_bited_our_data = json.dumps(encapsulated, indent=4)
        bited_our_data = not_yet_bited_our_data.encode()
        print("send: " + bited_our_data.decode())
        self.request.sendall(bited_our_data)


    def get_user_data (self, message):
        user_data = {
            "id": message["id"],
            "name": message["name"]
        }
        return user_data
    def list_of_people(self):
        list_of_peoples_name = []
        for action in actions:
            if action["type"] == "personadd":
                list_of_peoples_name.append({action["id_p"]: action["name"]})
            if action["type"] == "personrem":
                list_of_peoples_name.pop(action["id_p"])

        print (list_of_peoples_name)
        return list_of_peoples_name

    def get_id_from_pool(self):
        rand = random.randint(1, 999)
        for id_p in pool:
            if id_p == rand:
                rand = self.get_id_from_pool()
                break
        return rand

    def recvall(self, BUFF_SIZE=128):
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                # either 0 or end of data
                break
        return data

if __name__ == "__main__":
    global bash, people, lstmsgid, our_fp
    __file__ = os.path.dirname(os.path.abspath(__file__))
    bash = Bash(__file__ + "/.server_keypool", __file__ + "/.server_Config")
    #bash.create_private_key(nom="server_" + NAME_SERVER)
    while bash.get_list_prkeys_name() == []:
        print("Generating a private key...")
        server_key = bash.create_private_key(nom="server_" + NAME_SERVER)
        bash.save_data(server_key.fingerprint, "personal private key")

    our_fp = bash.get_list_prkeys_fingerprint()
    our_public_key = bash.export_key(our_fp)

    actions = []
    actions.append({
        "type": "server_key",
        "message": our_public_key,
        "id": 0, # el servidor serà l'usuari 0
        "name": bash.current_name(),
        "to": "all",
        "fp": bash.load_data("personal private key")
    })

    pool = []
    if len(sys.argv) >= 2:
        IP = str(sys.argv[1])
    if len(sys.argv) >= 3:
        PORT = int(sys.argv[2])
    buf = 256
    print("Press Ctrl+C to stop the server")

    try:
        with socketserver.TCPServer((IP, PORT), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            print("running on " + str(server.server_address))
            server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.shutdown()
