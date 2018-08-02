#!/usr/bin/env python3
import time
import datetime
import socket
import socketserver
import os
import json
import random
from bash import Bash 

class MyTCPHandler(socketserver.BaseRequestHandler):
        
    
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(256).strip()
        print("{} wrote:".format(self.client_address[0]))
        #self.data = str(self.data)
        print("recv: " + self.data.decode())
        self.Decide_what_to_do(self.data)
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())

    def Decide_what_to_do(self, bytedmessage):
        if bytedmessage != b'':
            message = json.loads(bytedmessage.decode())
            if message["type"] == "get_id_from_pool":
                self.send_back_one(self.get_id_from_pool()) 
            elif message["type"] == "command":
                self.send_back_one(message)
            else:
                actions.append(message)
                user_data = self.get_user_data(message)
                self.send_back_all(message["client_action_size"], user_data=user_data)
                self.process_new_action()
                

    def send_back_one(self, message="", type_message="message", extra = {}):
        
        encapsulated = {}
        encapsulated["all"] = []
        our_data = {
            "type": type_message,
            "message": message,
        }
        our_data.update(extra)
        """ arrextra = bash.dict_to_array(extra)
        for ext in arrextra:
            our_data[ext[0]] = ext[1] """
        
        encapsulated["all"].append(our_data)
        bited_our_data = json.dumps(encapsulated, indent=4).encode()
        print("send: " + bited_our_data.decode())
        self.request.sendall(bited_our_data)

    
    def send_back_all(self, index=0, user_data={}):
        encapsulated = {}
        encapsulated["all"] = []
        print("comencem a: " + str(index))

        for i in range(0, len(actions)):
            people = actions[i]["to"]
            #print(people)
            if i >= index:
                if people == "all" or people == user_data["id"]:
                    encapsulated["all"].append(actions[i])

            #if user_not_intended_to_see_this:
            #    encapsulated["all"].pop(i)
        
        bited_our_data = json.dumps(encapsulated,indent=4).encode()
        print("send: " + bited_our_data.decode())
        self.request.sendall(bited_our_data)
    
    def process_new_action(self):
        action = actions[len(actions) - 1]
        
    
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
                list_of_peoples_name.append({ action["id_p"] : action["name"] })
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
if __name__ == "__main__":
    global bash, people, lstmsgid, our_fp
    __file__ = os.path.dirname(os.path.abspath(__file__))
    bash = Bash(__file__ + "/.server_keypool")
    
    while bash.get_list_prkeys_name() == []:
        bash.create_private_key()
    our_fp = bash.get_list_prkeys_fingerprint()
    our_public_key = bash.export_key(our_fp)

    actions = []
    #OBJECTIU: posar la clau pública al principi per a cualsevol individu
    
    pool = []
    host = '0.0.0.0'
    port = 1234
    buf = 256
    print("press Ctrl+C to stop the server")
    try:
        with socketserver.TCPServer((host, port), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            print("running on " + str(server.server_address))
            server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.shutdown()
