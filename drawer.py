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
code = locale.getpreferredencoding()
# la classe
class Drawer(object):
# per tal de treballar bé, millor ja agafem les mesures de pantalla
    def __init__ (self, screen):
        self.height, self.width = screen.getmaxyx()

    def screen_window (self, screen, y0, x0, y1, x1):
        if (isinstance(y0, str)):
            y0=int(y0.replace("%","",1))
            y0=int(y0*self.height/100)
        if (isinstance(y1, str)):
            y1=int(y1.replace("%","",1))
            y1=int(y1*self.height/100)
        if (isinstance(x0, str)):
            x0=int(x0.replace("%","",1))
            x0=int(x0*self.width/100)
        if (isinstance(x1, str)):
            x1=int(x1.replace("%","",1))
            x1=int(x1*self.width/100)
        screen.addstr(y0,x0,str(y0)+","+str(x0))
        screen.addstr(y1,x1,str(y1)+","+str(x1))
        return
# dibuixa el menú. funciona bé, així que de moment no la tocarem.
    def main_menu(self, screen):
        screen.clear();
        screen.border();
        # aquesta part defineix el botó seleccionat de forma predeterminada
        # i inicialitza la variable del botó finalment seleccionat

        # per a mantenir uns retorns de dades cànon amb el programa, per a
        # aquest cas també es fan servir arrays. Però no faria falta
        selecteditem = [0,-1];
        selection = [-1,-1];
        while selection[0] < 0 and selection[1] < 0:
            #Array de 4
            selected=[0]*4
            # fem que el botó seleccionat estigui amb el color de fons i de lletra al revés
            selected[selecteditem[0]] = curses.A_REVERSE;
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
                    selecteditem[0] = (selecteditem[0] - 1) % 4;
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] + 1) % 4;
                elif action == ord("\n"):
                    selecteditem[1]=0
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
        # entrada per a crear claus
        list.append("++Nova Clau++")
        # la posarem a 0 girant tota la taula. Per a l'usuari sempre serà
        # l'ordre avitual perquè després les noves claus apareixeràn just a sota
        list.reverse()
        # nou esquema per a fer anar el sistema de selecció. Ara requereix d'arrays
        selecteditem = [0,-1];
        selection = [-1, -1];
        # la comfirmació es fa en les dos columnes de dades
        while selection[0] < 0 and selection[1] < 0:
            # creixement dinàmic de la taula. No podem tenir la taula vuida
            # afortunadament això no passarà perquè sempre tindrem la entrada
            # de una nova clau
            selected=[0]*len(list)
            selected[0]
            selected[selecteditem[0]] = curses.A_REVERSE;
            x=0
            # posem tots els correus en la pantalla en el bucle for
            for mail in list:
                screen.addstr(2+x,3, mail, selected[x])
                x+=1
            # refresquem la pantalla
            screen.refresh()
            try:
                # moure el cursor e iterar
                action = screen.getch();
                if action == curses.KEY_UP:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] - 1) % len(list);
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] + 1) % len(list);
                elif action == ord("q") or action == curses.KEY_EXIT:
                    # sortir de la pantalla
                    selecteditem[1]=0
                    selection = selecteditem
                elif action == ord("\n"):
                    # entrar en opció del menú
                    selecteditem[1]=1
                    selection = selecteditem
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
        return selection;
    # en desenvolupament
    def add_pkey (self, screen):
        self.screen_window(screen, "20%", "10%", "80%", "80%")
        screen.addstr(18,18, "why me")
        screen.refresh()
    # útil per a saber el valor numèric de les tecles del teclat.
    # imprimeix en pantalla el resultat
    def keyboardebugger (self, screen):
        # és una part molt autoexplicativa i que probablement acavarà desapareixent.
        # no mereix la pena comentar-ho
        text=""
        q=str(ord("q"))
        # només pels cànons del programa
        selection=[0,0]
        a=True
        while a :
            screen.clear();
            screen.border();
            screen.addstr(2,2,text)
            screen.addstr(3,2,q)
            screen.refresh();
            try:
                # només admet un botó, per a sortir al menú anterior
                action = screen.getch();
                if action == ord("\n"):
                    a=False
                # posar el botó en la variable en pantalla
                else:
                    text=str(action)
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
        # i retornem el resultat
        return selection
