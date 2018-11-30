#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# molta cosa per ferlo funcionar. alguna cosa pot ser que la tregui,
# he estat fet probes
import sys
import curses
import threading
import locale
import json
from pprint import pprint
# els altres dos scripts necessaris
# drawer dibuixa els menús i s'ocupa del teclat. això és degut
# a curses, el manager de terminal que estem fent servir.
from drawer import Drawer
# Aquest script s'encarrega de les crides a bash. tot made in Pol Marcet :3
# Disclaimer: si ens posem cisquillosos les llibreries no les he fetes jo XD
from bash import Bash
# Aquest és el main script
class EnigmaPol(object):
    # menú principal. de moment no té massa funcionalitat persé,
    # però anem fent
    def make_choice(self):
        #Mantenim un while per a que no surti de la aplicació sense el meu permís
        KeepGoing = True
        while KeepGoing:
            # dibuixem el menú i esperem que ens digui quina entrada l'usuari escolleix
            choice = drawer.main_menu(screen)[0]
            if choice == 0:
                self.client_administrator()
            elif choice == 1:
                self.configuration()
            elif choice == 2:
                # Cridem a la part de l'administrador gpg
                self.gpg_administrator()
            elif choice == 3:
                KeepGoing = False
    # el que farà en entrar al administrador de Claus
    def gpg_administrator (self):
        # while perquè estem en un menú
        while True:
            # aconsegueix una llista de claus
            is_list_empty=[False,False]
            list1 = bash.get_list_prkeys_name()
            list2 = bash.get_list_pukeys_name()
            if len(list2)<1:
                list2.append("--Buit--")
                is_list_empty[1]=True
            finalist=[list1,list2]
            # la ensenya. aquesta part és més complexa que l'altre menú.
            # esquema temporal de funcionalitat:
            # -> primera columna:
            #    -> fila en la que estem
            # -> segona columna:
            #    -> columna en la que estem
            # -> tercera columna:
            #    -> acció que es farà. correspon amb un botó
            #    -> 0: exit. Per tant trencaríem el loop
            #    -> 1: enter. fer alguna cosa si estem a 0 en les columnes útils
            #    -> 2: R. borrar la clau. Anem a veure com surt això
            choice = drawer.list_pkeys(screen, finalist)
            # Aquesta part està en desenvolupament
            # Hauria de tornar al menú anterior
            if choice[2] == 0:
                return
            elif choice == [0,0,1]:
                choice2 = drawer.add_pkey(screen)
                if choice2[0] != "":
                    bash.create_private_key(choice2[0],choice2[1])
            if choice[2] == 2:
                if choice[1]==1 and is_list_empty[1]==False:
                    bash.remove_pukey(id=choice[0])
                elif choice[1]==0 and is_list_empty[1]==False:
                    # per tal de que les id's de les claus coincideixin, ja que sinó
                    # són una més del compte per culpa de l'opció "nova clau"
                    choice[0]-=1
                    bash.remove_prkey(id=choice[0])

    def configuration(self):
        list1 = bash.get_list_prkeys_name()

        fp = bash.load_data("personal private key")
        fps = bash.get_list_prkeys_fingerprint()
        fps.reverse()
        try:
            name_selected_index = fps.index(fp)
        except ValueError:
            name_selected_index = 0
        #choice = drawer.keyboardebugger(screen)
        # Mapa de choice:
        # 0 --> clau a usar, per id. transformar a fingerprint
        # 1 --> enviar claus?
        # 2 --> acceptar claus? (NO/Preguntar)
        config = drawer.config(screen, list1, name_selected_index)
        # guardem la configuració
        #bash.save_data(config[1], "send public key")
        #bash.save_data(config[2], "recieve public keys")

        # aconseguim la fingerprint de la clau. en cas que borri claus, evitarem problemes
        fingerprints = bash.get_list_prkeys_fingerprint()
        fingerprints.reverse()
        fingerprint = fingerprints[config[0]]
        bash.save_data(fingerprint, "personal private key")
        #Json mode
        # data = {}
        # data["config"] = []
        # data["config"].append({
        #     "personal private key": fingerprint,
        #     "send public key": config[1],
        #     "recieve public keys": config[2]
        # })
        # bash.save_data(data)
    def client_administrator (self):
        #choice = drawer.colordebugger(screen)
        #primer demanem la ip i port
        choice = drawer.solicit_ip_port_pwd(screen)
        if choice[3] == True:
            drawer.client_screen(screen, [choice[0], choice[1], choice[2]])
# la primera funció cridada
# defineix variables glovals a tot el programa
def setup_enigmapol(stdscr):
    global drawer, screen, bash
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    screen = stdscr
    enigmapol = EnigmaPol()
    bash = Bash()
    drawer = Drawer(screen)
    # i crida al menú principal. no huríem de fer res a partir d'aquí
    enigmapol.make_choice()
# truquet per a assegurar-nos que és l'escript principal
# (osease: que l'usuari a arrencat el programa correcte)
if __name__ == "__main__":
    # per al control de menú cridem la funció així. inicialitza la finestra de curses
    curses.wrapper(setup_enigmapol)
    # per a ús purament debuggacional
    sys.exit(0)
