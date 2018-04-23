#!/bin/python3
# -*- coding: utf-8 -*-
# script que dibuixa al terminal. De moment és limitat, ja el farem més modular
import curses
import threading
import locale
import sys
import time
from datetime import datetime
locale.setlocale(locale.LC_ALL, '')

# la classe
class Drawer(object):
# per tal de treballar bé, millor ja agafem les mesures de pantalla
    def __init__ (self, screen):
        self.height, self.width = screen.getmaxyx()
# dibuixa el menú. funciona bé, així que de moment no la tocarem.
    def main_menu(self, screen):
        screen.clear();
        screen.border();
        # aquesta part defineix el botó seleccionat de forma predeterminada
        # i inicialitza la variable del botó finalment seleccionat
        selecteditem = 0;
        selection = -1;
        while selection < 0:
            #Array de 4
            selected=[0]*4
            # fem que el botó seleccionat estigui amb el color de fons i de lletra al revés
            selected[selecteditem] = curses.A_REVERSE;
            screen.addstr(int(self.height / 2 - 5), int(self.width / 2 - 8), "Enigma Pol V0.0");
            screen.addstr(int(self.height / 2 - 2), int(self.width / 2 - 6), "Connectar amb un Servidor", selected[0]);
            screen.addstr(int(self.height / 2 - 1), int(self.width / 2 - 3), "Crear un Servidor", selected[1]);
            screen.addstr(int(self.height / 2), int(self.width / 2 - 5), "Configurar Claus", selected[2]);
            screen.addstr(int(self.height / 2 + 1), int(self.width / 2 - 2), "Sortir", selected[3]);
            #important: sinó no apareix res en pantalla!
            screen.refresh();
            try:
                # moure el cursor e iterar
                action = screen.getch();
                if action == curses.KEY_UP:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem = (selecteditem - 1) % 4;
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem = (selecteditem + 1) % 4;
                elif action == ord("\n"):
                    selection = selecteditem
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
        # i retornem el resultat
        return selection
    # estic cansat i això és un caos. revisar i refactoritzar. :(
    def list_pkeys (self, screen, list):
        screen.clear()
        screen.border()
        for index in range(len(list)):
            screen.addstr(int(1+index), int(1), list[index])
            screen.addstr(1, self.width-10, "why me" + str(index));
        screen.addstr(1, self.width-10, list);
        keyboardinput = -1
        while keyboardinput < 0:
            screen.refresh();
            try:
                action = screen.getch();
                if action == curses.KEY_UP:
                    keyboardinput=0
            except KeyboardInterrupt:
                sys.exit()
        return;
