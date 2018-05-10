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

# dibuixa el menú. funciona bé, així que de moment no la tocarem.
    def main_menu(self, screen):
        screen.clear();
        text_of_the_menu=["Enigma Pol V0.0", "Connectar amb un Servidor", "Crear un Servidor", "Configurar Claus", "Sortir"]
        self.screen_window(screen,0,0,self.height-2,self.width-1,curses.color_pair(19)+curses.A_REVERSE);
        self.screen_window(screen,2000,2000,2003,2003)
        sizeinx=int(len(max(text_of_the_menu, key=len))/2)
        self.screen_window(screen,"~5","~"+str(sizeinx+2),"~5","~"+str(sizeinx+2),curses.color_pair(8)+curses.A_REVERSE);
        screen.addstr(2,2,str(sizeinx))
        checkvar1 = curses.has_colors()
        checkvar2 = curses.can_change_color()
        # aquesta part defineix el botó seleccionat de forma predeterminada
        # i inicialitza la variable del botó finalment seleccionat

        # per a mantenir uns retorns de dades cànon amb el programa, per a
        # aquest cas també es fan servir arrays. Però no faria falta
        selecteditem = [0,-1];
        selection = [-1,-1];
        lenghlist = 4
        while selection[0] < 0 and selection[1] < 0:
            #Array de 4
            selected=[curses.A_REVERSE+curses.color_pair(8)]*lenghlist
            # fem que el botó seleccionat estigui amb el color de fons i de lletra al revés
            selected[selecteditem[0]] = curses.A_REVERSE+curses.color_pair(204);
            screen.addstr(int(self.height / 2 - 5), int(self.width / 2 - (len(text_of_the_menu[0])/2)), text_of_the_menu[0], curses.A_REVERSE+curses.color_pair(8));
            screen.addstr(int(self.height / 2 - 2), int(self.width / 2 - (len(text_of_the_menu[1])/2)), text_of_the_menu[1], selected[0]);
            screen.addstr(int(self.height / 2 - 1), int(self.width / 2 - (len(text_of_the_menu[2])/2)), text_of_the_menu[2], selected[1]);
            screen.addstr(int(self.height / 2 + 0), int(self.width / 2 - (len(text_of_the_menu[3])/2)), text_of_the_menu[3], selected[2]);
            screen.addstr(int(self.height / 2 + 1), int(self.width / 2 - (len(text_of_the_menu[4])/2)), text_of_the_menu[4], selected[3]);
            #important: sinó no apareix res en pantalla!
            screen.refresh();
            try:
                # moure el cursor e iterar
                action = screen.getch();
                if action == curses.KEY_UP:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist;
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist;
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
        titol1="Claus Privades:"
        self.screen_window(screen,0,0,self.height-2,self.width-1,curses.color_pair(19)+curses.A_REVERSE);
        self.screen_window(screen,1,1, 5+len(list), 4+len(titol1),curses.color_pair(8)+curses.A_REVERSE);
        self.screen_window(screen,"90%","~40%","+3","~40%",curses.color_pair(8)+curses.A_REVERSE);

        screen.addstr(1,3, titol1, curses.A_REVERSE+curses.color_pair(8))
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
            lenghlist = len(list)
            selected=[curses.A_REVERSE+curses.color_pair(8)]*lenghlist
            #selected[0]
            selected[selecteditem[0]] = curses.A_REVERSE+curses.color_pair(204);
            x=0
            # posem tots els correus en la pantalla en el bucle for
            for mail in list:
                screen.addstr(3+x,3, mail, selected[x])
                x+=1
            # refresquem la pantalla
            screen.refresh()
            try:
                # moure el cursor e iterar
                action = screen.getch();
                if action == curses.KEY_UP:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist;
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist;
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
        lenghlist = 2
        selecteditem = [0,-1];
        selection = [-1, -1];
        valuesgiven=[""]*lenghlist
        valueskeysize=["1024","2048","4096"]
        valueskeysizeselected = 2
        # la comfirmació es fa en les dos columnes de dades
        while selection[0] < 0 and selection[1] < 0:
            self.screen_window(screen, "~5", "~15", "~5", "~15")
            selected=[0]*lenghlist

            selected[selecteditem[0]] = curses.A_REVERSE;
            screen.addstr(self.percentwin("50%", True)+3,self.percentwin("50%", False)-14, "Tamany de la clau: "+"<"+valueskeysize[valueskeysizeselected]+">", selected[1])
            screen.addstr(self.percentwin("50%", True),self.percentwin("50%", False)-14, "Nom: "+valuesgiven[0], selected[0])
            # refresquem la pantalla
            screen.refresh()
            try:
                # moure el cursor e iterar
                action = screen.getch();
                if action == curses.KEY_UP:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist;
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist;
                elif action== curses.KEY_RIGHT:
                    if selecteditem[0]==1:
                        valueskeysizeselected = (valueskeysizeselected+1) % len(valueskeysize)
                elif action== curses.KEY_LEFT:
                    if selecteditem[0]==1:
                        valueskeysizeselected = (valueskeysizeselected-1) % len(valueskeysize)
                elif action == curses.KEY_EXIT or action == ord("\n") or action == 27:
                    # sortir de la pantalla
                    selecteditem[1]=0
                    valuesgiven[1]=valueskeysize[valueskeysizeselected]
                    selection = selecteditem
                    # entrar en opció del menú
                    selecteditem[1]=1
                    selection = selecteditem
                elif action == 127:
                    if selecteditem[0]==0:
                        valuesgiven[0]=valuesgiven[0][:-1]
                else:
                    if selecteditem[0]==0:
                        valuesgiven[0]+=chr(action)

            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
        return valuesgiven;
    def complexwin (self, i0, i1, is_y):
        if (isinstance(i0,str)):
            if "~" in i0:
                i0=i0.replace("~","",1)
                i0=self.percentwin("50%", is_y)-int(self.percentwin(i0, is_y))-1
            else:
                i0=self.percentwin(i0, is_y)
            i0=int(i0)
        if (isinstance(i1,str)):
            if "+" in i1:
                i1=i1.replace("+","",1)
                add=i0
            else:
                add=0
            if "~" in i1:
                i1=i1.replace("~","",1)
                i1=self.percentwin("50%", is_y)+int(self.percentwin(i1, is_y))
            else:
                i1=self.percentwin(i1, is_y)
            i1=int(i1)
            i1=i1+add
        if i0<0:
            i1-=(i0)
            i0-=(i0)
        a=0
        if is_y:
            a=self.height
            if i1>a:
                i0-=(i1-a)+2
                i1-=(i1-a)+2
        else:
            a=self.width
            if i1>a:
                i0-=(i1-a)+1
                i1-=(i1-a)+1
        return i0, i1

    def percentwin (self, percent, is_y):
        if isinstance(percent, str):
            if "%" in percent :
                percent=int(percent.replace("%","",1))
                if (is_y):
                    percent=int(percent*self.height/100)
                else:
                    percent=int(percent*self.width/100)
        return percent
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
    def colordebugger (self,screen):
        checkvar1 = curses.has_colors()
        checkvar2 = curses.can_change_color()
        COLOR_NOW=curses.COLOR_PAIRS
        startwhitha0=0
        a=True
        while a :
            screen.clear();
            self.screen_window(screen,0,0,self.height-2,self.width-1,curses.color_pair(19)+curses.A_REVERSE);
            screen.addstr(2,2,str(checkvar1))
            screen.addstr(3,2,str(checkvar2))
            screen.addstr(4,2,str(curses.COLORS))
            screen.addstr(5,2,str(curses.COLOR_PAIRS))
            starting=startwhitha0
            for y in range(0,36):
                for x in range(0,32):
                    screen.addstr(y+10,5*x+15,str(startwhitha0),curses.color_pair(startwhitha0))
                    startwhitha0=1 + startwhitha0 % COLOR_NOW
            startwhitha0=starting
            try:
                # només admet un botó, per a sortir al menú anterior
                action = screen.getch();
                if action == ord("\n"):
                    a=False
                elif action == curses.KEY_UP:
                    startwhitha0 = (startwhitha0 - 32) % COLOR_NOW;
                elif action == curses.KEY_DOWN:
                    startwhitha0 = (startwhitha0 + 32) % COLOR_NOW;
                elif action== curses.KEY_RIGHT:
                    startwhitha0 = (startwhitha0 - 256) % COLOR_NOW;
                elif action== curses.KEY_LEFT:
                    startwhitha0 = (startwhitha0 + 256) % COLOR_NOW;
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
    def screen_window (self, screen, y0, x0, y1, x1, data=0):
        y0, y1 = self.complexwin(y0,y1, True)
        x0, x1 = self.complexwin(x0,x1, False)
        # intercambiar les x en cas que x1 sigui més petita que x0
        if (x0>x1):
            tempx0=x0
            x0=x1
            x1=tempx0
        # intercambiar les y en cas que y1 sigui més petita que y0
        if (y0>y1):
            tempy0=y0
            y0=y1
            y1=tempy0
        numslash=x1-x0
        slash=""
        space=""
        while (numslash>=0):
            slash+="─"
            space+=" "
            numslash -= 1
        space = space[:-2]
        screen.addstr(y0,x0,slash,data)
        screen.addstr(y1,x0,slash,data)
        slash="│"
        for i in range(y0+1,y1):
            screen.addstr(i,x0,slash+space+slash,data)
        screen.addstr(y0,x0,"┌",data);
        screen.addstr(y0,x1,"┐",data);
        screen.addstr(y1,x0,"└",data);
        screen.addstr(y1,x1,"┘",data);
        return
