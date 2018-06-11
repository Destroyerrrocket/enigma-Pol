#!/bin/python3
# -*- coding: utf-8 -*-
# script que dibuixa al terminal. De moment és limitat, ja el farem més modular
import curses
import threading
import locale
import sys
import time
from datetime import datetime
from client_terminal import Client_terminal
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()
# la classe
class Drawer(object):
# per tal de treballar bé, millor ja agafem les mesures de pantalla
    def __init__ (self, screen):
        self.height, self.width = screen.getmaxyx()
        self.use_colors = curses.has_colors()
        self.can_set_colors = curses.can_change_color()

# dibuixa el menú. funciona bé, així que de moment no la tocarem.
    def main_menu(self, screen):
        screen.clear()
        text_of_the_menu=["Enigma Pol V0.0", "Connectar amb un Servidor", "Crear un Servidor", "Configurar Claus", "Sortir"]
        self.screen_window(screen,0,0,self.height-2,self.width-1,curses.color_pair(5)+curses.A_REVERSE)
        sizeinx=int(len(max(text_of_the_menu, key=len))/2)
        self.screen_window(screen,"~5","~"+str(sizeinx+2),"~5","~"+str(sizeinx+2),curses.color_pair(8)+curses.A_REVERSE)
        
        # aquesta part defineix el botó seleccionat de forma predeterminada
        # i inicialitza la variable del botó finalment seleccionat

        # per a mantenir uns retorns de dades cànon amb el programa, per a
        # aquest cas també es fan servir arrays. Però no faria falta
        selecteditem = [0,-1]
        selection = [-1,-1, -1]
        lenghlist = 4
        while max(selection) < 0:
            #Array de 4
            selected=[curses.A_REVERSE+curses.color_pair(8)]*lenghlist
            # fem que el botó seleccionat estigui amb el color de fons i de lletra al revés
            selected[selecteditem[0]] = curses.A_REVERSE+curses.color_pair(204)
            screen.addstr(int(self.height / 2 - 5), int(self.width / 2 - (len(text_of_the_menu[0])/2)), text_of_the_menu[0], curses.A_REVERSE+curses.color_pair(8))
            screen.addstr(int(self.height / 2 - 2), int(self.width / 2 - (len(text_of_the_menu[1])/2)), text_of_the_menu[1], selected[0])
            screen.addstr(int(self.height / 2 - 1), int(self.width / 2 - (len(text_of_the_menu[2])/2)), text_of_the_menu[2], selected[1])
            screen.addstr(int(self.height / 2 + 0), int(self.width / 2 - (len(text_of_the_menu[3])/2)), text_of_the_menu[3], selected[2])
            screen.addstr(int(self.height / 2 + 1), int(self.width / 2 - (len(text_of_the_menu[4])/2)), text_of_the_menu[4], selected[3])
            #important: sinó no apareix res en pantalla!
            screen.refresh()
            try:
                # moure el cursor e iterar
                action = screen.get_wch()
                if action == curses.KEY_UP:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist
                elif action == "\n":
                    selecteditem[1]=0
                    selection = selecteditem
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
        # i retornem el resultat
        return selection
    def list_pkeys (self, screen, listall):
        # borrem la pantalla
        screen.clear()
        # el títol del menú 1
        titol1="Claus Privades:"
        # el títol del menú 2
        titol2="Claus Públiques:"
        # el text de les instruccions
        text_of_controls="[R]: Borrar, [E]: Exportar, [I] Importar"
        # en cas de que el menú 2 no tingui res, afegirem una variable per tal de que no exploti
        if len(listall[1])<1:
            listall[1][0]="--Buit--"

        # entrada per a crear claus
        listall[0].append("++Nova Clau++")
        # la posarem a 0 girant tota la taula. Per a l'usuari sempre serà
        # l'ordre avitual perquè després les noves claus apareixeràn just a sota
        listall[0].reverse()
        listall[1].reverse()
        # sizeinx=valors per a calcular distàncies de dibuix en la x, les poso a part per a fer el codi més llegible
        # aquí calculem el tamany de la finestra 1 per tal que el text no se surti del rectangle
        sizeinx=int(len(max(listall[0], key=len)))
        # rectangle blau que serà el fons.
        self.screen_window(screen,0,0,self.height-2,self.width-1,curses.color_pair(5)+curses.A_REVERSE)
        # crea la finestra 1, del tamany relatiu al nombre de claus
        self.screen_window(screen,1,1, 4+len(listall[0]), sizeinx+4,curses.color_pair(8)+curses.A_REVERSE)
        # calculem el tamany de la finestra 2 per tal que el text no es surti
        sizeinx2=int(len(max(listall[1], key=len)))
        if sizeinx2 < 15:
            sizeinx2=15
        # crea la finestra 2
        self.screen_window(screen,1, sizeinx+7, 4+len(listall[1]), sizeinx2+sizeinx+7+3,curses.color_pair(8)+curses.A_REVERSE)
        # crea la finestra 3. Aquesta és la de les instruccions per al gestor
        self.screen_window(screen,self.height-8,"~40%","+4","~40%",curses.color_pair(8)+curses.A_REVERSE)
        # calcular el """"centre"""" per al text de les instruccions. És modular així que no tindré que cambiar-ho
        sizeinx3=int(self.width / 2 - (len(text_of_controls)/2))
        # Posem el titol i el text de les instruccions
        screen.addstr(self.height-8,self.percentwin("10%",False)+2,"Instruccions: ",curses.A_REVERSE+curses.color_pair(8))
        screen.addstr(self.height-6,sizeinx3,text_of_controls,curses.A_REVERSE+curses.color_pair(8))
        # titol de la finestra 1
        screen.addstr(1,2, titol1, curses.A_REVERSE+curses.color_pair(8))
        screen.addstr(1,2+sizeinx+6, titol2, curses.A_REVERSE+curses.color_pair(8))

        # nou esquema per a fer anar el sistema de selecció. Ara requereix d'arrays
        selecteditem = [0, 0,-1]
        selection = [-1, -1, -1]
        # la comfirmació es fa en les dos columnes de dades
        while max(selection) < 0:
            # creixement dinàmic de la taula. No podem tenir la taula vuida
            # afortunadament això no passarà perquè sempre tindrem la entrada
            # de una nova clau i la de que està buida. Podriem integrar un
            # comprobador, però llavors les finestres també estarien
            # desorientades. El món té sentit així
            lenghlist1 = len(listall[0])
            lenghlist2 = len(listall[1])
            selected1=[curses.A_REVERSE+curses.color_pair(8)]*lenghlist1
            selected2=[curses.A_REVERSE+curses.color_pair(8)]*lenghlist2
            # aquí, tenint en compte en quina finestra estem, determinarà
            # quina clau està seleccionada.
            if selecteditem[1]==0:
                lenghlist = lenghlist1
                selected1[selecteditem[0]] = curses.A_REVERSE+curses.color_pair(204)
            elif selecteditem[1]==1:
                lenghlist = lenghlist2
                selected2[selecteditem[0]] = curses.A_REVERSE+curses.color_pair(204)
            #selected[0]
            x=0
            # posem tots els correus en la pantalla en el bucle for
            for mail in listall[0]:
                screen.addstr(3+x,3, mail, selected1[x])
                x+=1
            # calculem la llargada de la finestra 1. per fer-ho cal tenir en compte el mail més llarg
            sizeinx=int(len(max(listall[0], key=len)))
            x=0
            # posem tots els correus en la pantalla en el bucle for
            for mail in listall[1]:
                screen.addstr(3+x,sizeinx+9, mail, selected2[x])
                x+=1
            # refresquem la pantalla
            screen.refresh()
            # SECCIÓ D'INTERACCIÓ DE L'USUARI
            try:
                # moure el cursor e iterar
                action = screen.get_wch()
                if action == curses.KEY_UP:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist
                elif action == curses.KEY_LEFT:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[1] = (selecteditem[1] - 1) % 2
                    if selecteditem[0] > len(listall[selecteditem[1]])-1:
                        selecteditem[0] = len(listall[selecteditem[1]])-1
                elif action == curses.KEY_RIGHT:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[1] = (selecteditem[1] + 1) % 2

                    if selecteditem[0] > len(listall[selecteditem[1]])-1:
                        selecteditem[0] = len(listall[selecteditem[1]])-1
                elif action == "q" or action == curses.KEY_EXIT:
                    # sortir de la pantalla
                    selecteditem[2]=0
                    selection = selecteditem
                elif action == "\n":
                    # entrar en opció del menú
                    selecteditem[2]=1
                    selection = selecteditem
                elif action == "r":
                    # entrar en opció del menú
                    selecteditem[2]=2
                    selection = selecteditem
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
        return selection
    # en desenvolupament
    def add_pkey (self, screen):
        # declarem moltes variables. moltes són prou autoexplicatives
        lenghlist = 2
        selecteditem = [0,-1]
        selection = [-1, -1, -1]
        valuesgiven=[""]*lenghlist
        # bits que axceptaré. No confio en que l'usuari els possi bé
        valueskeysize=["1024","2048","4096"]
        valueskeysizeselected = 2
        # la comfirmació es fa en les dos columnes de dades
        while max(selection) < 0:
            # crearem una finestra. Està dintre del bucle per a evitar que quan
            # l'usuari borri les lletres es quedin en pantalla. No vull que es
            # pensin que el programa està trencat :)
            self.screen_window(screen, "~5", "~15", "~5", "~15",curses.A_REVERSE+curses.color_pair(8))
            # la opció seleccionada
            selected=[curses.A_REVERSE+curses.color_pair(8)]*(lenghlist+1)
            selected[selecteditem[0]] = curses.A_REVERSE+curses.color_pair(204)
            # creem les opcions del menú. Titol, opció 2 i opció 1. Aquest ordre
            # és per a donar a l'usuari la il·lució que el cursor està en el que
            # estàn escribint. No afecta massa el codi i prefereixo que quedi bonic
            screen.addstr(self.percentwin("50%", True)-6,self.percentwin("50%", False)-14, "Crear nova clau privada: ", selected[2])
            screen.addstr(self.percentwin("50%", True)+3,self.percentwin("50%", False)-14, "Tamany de la clau: "+"<"+valueskeysize[valueskeysizeselected]+">", selected[1])
            screen.addstr(self.percentwin("50%", True),self.percentwin("50%", False)-14, "Nom: "+valuesgiven[0], selected[0])
            # refresquem la pantalla
            screen.refresh()
            # PART D'INTERACCIÓ
            try:
                # moure el cursor e iterar
                action = screen.get_wch()
                if action == curses.KEY_UP:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist
                elif action == curses.KEY_DOWN:
                    # VISCA LA PROGRAMACIÓ MODULAR!
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist
                elif action== curses.KEY_RIGHT:
                    if selecteditem[0]==1:
                        valueskeysizeselected = (valueskeysizeselected+1) % len(valueskeysize)
                elif action== curses.KEY_LEFT:
                    if selecteditem[0]==1:
                        valueskeysizeselected = (valueskeysizeselected-1) % len(valueskeysize)
                elif action == curses.KEY_EXIT or action == "\n" or action == "\x1b":
                    # simplement li diem el tamany de la clau i li diem que ja hem cabat al incomplir el while
                    valuesgiven[1]=valueskeysize[valueskeysizeselected]
                    selection = selecteditem
                # borrar un caràcter del text del nom.
                elif action == "\x7f":
                    if selecteditem[0]==0:
                        valuesgiven[0]=valuesgiven[0][:-1]
                # Aquí assignem la tecla al text del nom.
                else:
                    if selecteditem[0]==0:
                        valuesgiven[0]+=action

            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
        return valuesgiven
    # útil per a saber el valor numèric de les tecles del teclat.
    # imprimeix en pantalla el resultat
    def keyboardebugger (self, screen):
        # és una part molt autoexplicativa i que probablement acavarà desapareixent.
        # no mereix la pena comentar-ho
        text=""
        q=str(ord("\n"))
        # només pels cànons del programa
        selection=[0,0]
        a=True
        while a :
            screen.clear()
            screen.border()
            screen.addstr(2,2,"%s: %s\n" % (repr(text), type(text)))
            screen.addstr(3,2,q)
            screen.refresh()
            try:
                # només admet un botó, per a sortir al menú anterior
                action = screen.get_wch()
                if action == "\n":
                    a=False
                # posar el botó en la variable en pantalla
                else:
                    text=action
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
        # i retornem el resultat
        return selection

    def solicit_ip_port(self, screen):
        # Programaré aquest menú més endavant
        return ["0.0.0.0", 1234]
    def client_screen(self, screen, address):
        screen.clear()
        client = Client_terminal(address[0], address[1], [self.width-2, self.height-7])
        rwitten_data = ""
        while True:
            self.screen_window(screen, 0, 0, self.height - 2, self.width - 1, curses.color_pair(8) + curses.A_REVERSE)
            screen.addstr(self.height - 4, 0,"├" + "─" * (self.width - 2) + "┤", curses.color_pair(8) + curses.A_REVERSE)
            screen.addstr(2, 0, "├" + "─" * (self.width - 2) + "┤", curses.color_pair(8) + curses.A_REVERSE)
            screen.addstr(1, 1, "Connectat: "+str(client.ip)+":"+str(client.port)+" ("+client.State+")", curses.color_pair(8) + curses.A_REVERSE)
            x=0
            for line in client.terminfo:
                screen.addstr(
                    3+x, 1, line, curses.color_pair(8) + curses.A_REVERSE)
                x += 1
            
            screen.refresh()
            try:
                action = screen.get_wch()
                if action == "\n":
                    client.send_message(rwitten_data)
                    rwitten_data = ""
                elif action == "\x7f":
                    if rwitten_data != "":
                        rwitten_data[0] = rwitten_data[0][:-1]
                else:
                    rwitten_data += action
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
            
        

    def colordebugger (self,screen):
        # Aquest programa està pensat per a funcionar sota condicions especifiques. no hem mereix la pena comentar-lo
        checkvar1 = curses.has_colors()
        checkvar2 = curses.can_change_color()
        COLOR_NOW=curses.COLOR_PAIRS
        startwhitha0=0
        a=True
        while a :
            screen.clear()
            self.screen_window(screen, 0, 0, self.height - 2, self.width - 1, curses.color_pair(5) + curses.A_REVERSE)
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
                action = screen.get_wch()
                if action == "\n":
                    a=False
                elif action == curses.KEY_UP:
                    startwhitha0 = (startwhitha0 - 32) % COLOR_NOW
                elif action == curses.KEY_DOWN:
                    startwhitha0 = (startwhitha0 + 32) % COLOR_NOW
                elif action== curses.KEY_RIGHT:
                    startwhitha0 = (startwhitha0 + 256) % COLOR_NOW
                elif action== curses.KEY_LEFT:
                    startwhitha0 = (startwhitha0 - 256) % COLOR_NOW
            # si decideix sortir de forma prematura
            except KeyboardInterrupt:
                sys.exit()
    def screen_window (self, screen, y0, x0, y1, x1, data=0):
        # he creat un sistema més complexe per a fer les transformacions.
        # admet, com a str, "+", "~", "%" | que el que fan és:
        # sumar | restar/sumar al 50% | transformar un % en un valor útil.
        # es poden combinar, però fes-ho amb seny.
        # també té un sistema de seguretat per a evitar fer finestres fora de la
        # pantalla, però està en desenvolupament i falla, així que no hem siguis
        # bago i programa bé
        y0, y1 = self.complexwin(y0,y1, True)
        x0, x1 = self.complexwin(x0,x1, False)
        # per si el programador que hem fa servir es dona un cop fort al cap,
        # millor ser nosaltres els intel·ligents
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
        # número de "-" de la barra de adalt
        numslash=x1-x0
        # calculem els caracters a usar
        slash="─"*numslash
        space=" "*numslash
        # restem 1 als espais perquè hi ha un borde de 1 a cada vanda "|". Un vorde ja està descomptat
        space = space[:-1]
        # primer la linia de dalt i abaix
        screen.addstr(y0,x0,slash,data)
        screen.addstr(y1,x0,slash,data)
        slash="│"
        #la resta de linies
        for i in range(y0+1,y1):
            screen.addstr(i,x0,slash+space+slash,data)
        # fem les cantonades. per si en un futur vull facilitarme la feina
        screen.addstr(y0,x0,"┌",data)
        screen.addstr(y0,x1,"┐",data)
        screen.addstr(y1,x0,"└",data)
        screen.addstr(y1,x1,"┘",data)
        return
    def complexwin (self, i0, i1, is_y):
        # moltes operacions matematiques. És una funció interna.
        # No es toca si segueix funcionant
        add=0
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
        else:
            a=self.width
        if is_y:
            if i1>a:
                i0-=(i1-a)+2
                i1-=(i1-a)+2
        else:
            if i1>a:
                i0-=(i1-a)+1
                i1-=(i1-a)+1
        return i0, i1
    def percentwin (self, percent, is_y):
        # moltes operacions matematiques. És una funció interna.
        # No es toca si segueix funcionant
        if isinstance(percent, str):
            if "%" in percent :
                percent=int(percent.replace("%","",1))
                if (is_y):
                    percent=int(percent*self.height/100)
                else:
                    percent=int(percent*self.width/100)
        return percent
