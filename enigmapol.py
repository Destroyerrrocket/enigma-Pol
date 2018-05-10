#!/bin/python3
# -*- coding: utf-8 -*-
# molta cosa per ferlo funcionar. alguna cosa pot ser que la tregui,
# he estat fet probes
import sys
import curses
import threading
import locale
from pprint import pprint
# els altres dos scripts necessaris
# drawer dibuixa els menús i s'ocupa (de moment) del teclat. això és degut
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
                # TODO fer client
                self.client_administrator()
            elif choice == 1:
                # TODO fer servidor
                # de moment només serveix per a debugar les tecles del teclat.
                # Que no és algo especialment útil.
                self.server_administrator()
            elif choice == 2:
                # TODO fer administrador
                # Ja comença a agafar forma. Encara queda fèina a fer
                # Cridem a la part de l'administrador gpg
                self.gpg_administrator();
            elif choice == 3:
                KeepGoing = False
    # el que farà en entrar al administrador de Claus
    def gpg_administrator (self):
        # while perquè estem en un menú
        KeepGoing = True
        while KeepGoing:
            # aconsegueix una llista de claus
            list = bash.get_list_pkeys_mail()
            # la ensenya. aquesta part és més complexa que l'altre menú.
            # esquema temporal de funcionalitat:
            # -> primera columna:
            #    -> 0: Crear nova clau
            # -> segona columna:
            #    -> 0: exit. Per tant trencaríem el loop
            #    -> 1: enter. fer alguna cosa si estem a 0 en les columnes útils
            choice = drawer.list_pkeys(screen, list)
            # Aquesta part està en desenvolupament
            # Hauria de tornar al menú anterior
            if choice == [0,0]:
                return;
            elif choice == [0,1]:
                choice2 = drawer.add_pkey(screen)
                if choice2[0] != "":
                    bash.create_private_key(choice2[0],choice2[1])
    def server_administrator (self):
        choice = drawer.keyboardebugger(screen)
    def client_administrator (self):
        choice = drawer.colordebugger(screen)
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
    # per al control de menú cridem la funció així. No m'agrada. Però funciona
    curses.wrapper(setup_enigmapol)
    # per a ús purament debuggacional
    #bash = Bash()
    #print(list)
    #list = bash.get_list_pkeys_name()
    sys.exit(0);
