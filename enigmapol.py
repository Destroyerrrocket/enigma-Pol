#!/bin/python3
# -*- coding: utf-8 -*-
# molta cosa per ferlo funcionar. alguna cosa pot ser que la tregui,
# he estat fet probes
import sys
import curses
import threading
import locale
# els altres dos scripts necessaris
# drawer dibuixa els menús i s'ocupa (de moment) del teclat. això és degut
# a curses, el manager de terminal que estem fent servir.
from drawer import Drawer
# Aquest script s'encarrega de les crides a bash. tot made in Pol Marcet :3
from bash import Bash
# Aquest és el main script
class EnigmaPol(object):
    # menú principal. de moment no té massa funcionalitat persé,
    # però anem fent
    def make_choice(self):
        #perquè hem surt del while? IDK
        while True:
            choice = drawer.main_menu(screen)
            if choice == 0:
                # TODO fer client
                return;
            elif choice == 1:
                # TODO fer servidor
                return;
            elif choice == 2:
                # TODO fer administrador
                # de moment fa el que vol :(
                self.gpg_administrator();
                return;
            elif choice == 3:
                sys.exit();
    # el que farà en entrar al administrador de claus
    def gpg_administrator (self):
        # aconsegueix una llista de claus
        list = bash.get_list_pkeys()
        # la hauria d'ensenyar. però no ho fa
        drawer.list_pkeys(screen, list)
# la primera funció cridada
# defineix variables glovals a tot el programa
def setup_enigmapol(stdscr):
    global drawer, screen, bash
    screen = stdscr
    enigmapol = EnigmaPol()
    bash = Bash()
    drawer = Drawer(screen)
    # i crida al menú principal. no huríem de fer res a partir d'aquí
    enigmapol.make_choice()
# truquet per a assegurar-nos que és l'escript principal
# (asease: que l'usuari a arrencat el programa correcte)
if __name__ == "__main__":
    # per al control de menú cridem la funció així. No m'agrada. Però funciona
    curses.wrapper(setup_enigmapol)
    # per a ús purament debuggacional
    bash = Bash()
    list = bash.get_list_pkeys()
    for index in range(len(list)):
        print(list[index])
    sys.exit(1);
