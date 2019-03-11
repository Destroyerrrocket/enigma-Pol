#!/bin/python3
# -*- coding: utf-8 -*-
import curses
import threading
import locale
import sys
import time
from client_terminal import Client_terminal
from threading import Thread

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


class Drawer(object):
    def __init__(self, screen):
        self.height, self.width = screen.getmaxyx()
        self.use_colors = curses.has_colors()
        self.can_set_colors = curses.can_change_color()

    def main_menu(self, screen):
        screen.clear()
        text_of_the_menu = [
            "Enigma Pol V1.0", "Connectar amb un servidor", "Configuració",
            "Configurar claus", "Sortir"
        ]
        self.screen_window(screen, 0, 0, self.height - 2, self.width - 1,
                           curses.color_pair(5) + curses.A_REVERSE)
        sizeinx = int(len(max(text_of_the_menu, key=len)) / 2)
        self.screen_window(screen, "~5", "~" + str(sizeinx + 2), "~5",
                           "~" + str(sizeinx + 2),
                           curses.color_pair(8) + curses.A_REVERSE)

        selecteditem = [0, -1]
        selection = [-1, -1, -1]
        lenghlist = 4
        while max(selection) < 0:
            selected = [curses.A_REVERSE + curses.color_pair(8)] * lenghlist
            selected[selecteditem[
                0]] = curses.A_REVERSE + curses.color_pair(204)
            screen.addstr(
                int(self.height / 2 - 5),
                int(self.width / 2 - (len(text_of_the_menu[0]) / 2)),
                text_of_the_menu[0], curses.A_REVERSE + curses.color_pair(8))
            screen.addstr(
                int(self.height / 2 - 2),
                int(self.width / 2 - (len(text_of_the_menu[1]) / 2)),
                text_of_the_menu[1], selected[0])
            screen.addstr(
                int(self.height / 2 - 1),
                int(self.width / 2 - (len(text_of_the_menu[2]) / 2)),
                text_of_the_menu[2], selected[1])
            screen.addstr(
                int(self.height / 2 + 0),
                int(self.width / 2 - (len(text_of_the_menu[3]) / 2)),
                text_of_the_menu[3], selected[2])
            screen.addstr(
                int(self.height / 2 + 1),
                int(self.width / 2 - (len(text_of_the_menu[4]) / 2)),
                text_of_the_menu[4], selected[3])
            screen.refresh()
            try:
                action = screen.get_wch()
                if action == curses.KEY_UP:
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist
                elif action == curses.KEY_DOWN:
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist
                elif action == "\n":
                    selecteditem[1] = 0
                    selection = selecteditem
            except KeyboardInterrupt:
                sys.exit()
        return selection

    def list_pkeys(self, screen, listall):
        screen.clear()
        titol1 = "Claus Privades:"
        titol2 = "Claus Públiques:"
        text_of_controls = "[R]: Borrar"
        if len(listall[1]) < 1:
            listall[1][0] = "--Buit--"

        listall[0].append("++Nova Clau++")
        listall[0].reverse()
        listall[1].reverse()
        sizeinx = int(len(max(listall[0], key=len)))
        self.screen_window(screen, 0, 0, self.height - 2, self.width - 1,
                           curses.color_pair(5) + curses.A_REVERSE)
        self.screen_window(screen, 1, 1, 4 + len(listall[0]), sizeinx + 4,
                           curses.color_pair(8) + curses.A_REVERSE)
        sizeinx2 = int(len(max(listall[1], key=len)))
        if sizeinx2 < 15:
            sizeinx2 = 15
        self.screen_window(screen, 1, sizeinx + 7, 4 + len(listall[1]),
                           sizeinx2 + sizeinx + 7 + 3,
                           curses.color_pair(8) + curses.A_REVERSE)
        self.screen_window(screen, self.height - 8, "~40%", "+4", "~40%",
                           curses.color_pair(8) + curses.A_REVERSE)
        sizeinx3 = int(self.width / 2 - (len(text_of_controls) / 2))
        screen.addstr(self.height - 8,
                      self.percentwin("10%", False) + 2, "Instruccions: ",
                      curses.A_REVERSE + curses.color_pair(8))
        screen.addstr(self.height - 6, sizeinx3, text_of_controls,
                      curses.A_REVERSE + curses.color_pair(8))
        screen.addstr(1, 2, titol1, curses.A_REVERSE + curses.color_pair(8))
        screen.addstr(1, 2 + sizeinx + 6, titol2,
                      curses.A_REVERSE + curses.color_pair(8))

        selecteditem = [0, 0, -1]
        selection = [-1, -1, -1]
        while max(selection) < 0:
            lenghlist1 = len(listall[0])
            lenghlist2 = len(listall[1])
            selected1 = [curses.A_REVERSE + curses.color_pair(8)] * lenghlist1
            selected2 = [curses.A_REVERSE + curses.color_pair(8)] * lenghlist2
            if selecteditem[1] == 0:
                lenghlist = lenghlist1
                selected1[selecteditem[
                    0]] = curses.A_REVERSE + curses.color_pair(204)
            elif selecteditem[1] == 1:
                lenghlist = lenghlist2
                selected2[selecteditem[
                    0]] = curses.A_REVERSE + curses.color_pair(204)
            #selected[0]
            x = 0
            for mail in listall[0]:
                screen.addstr(3 + x, 3, mail, selected1[x])
                x += 1
            sizeinx = int(len(max(listall[0], key=len)))
            x = 0
            for mail in listall[1]:
                screen.addstr(3 + x, sizeinx + 9, mail, selected2[x])
                x += 1
            screen.refresh()
            try:
                action = screen.get_wch()
                if action == curses.KEY_UP:
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist
                elif action == curses.KEY_DOWN:
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist
                elif action == curses.KEY_LEFT:
                    selecteditem[1] = (selecteditem[1] - 1) % 2
                    if selecteditem[0] > len(listall[selecteditem[1]]) - 1:
                        selecteditem[0] = len(listall[selecteditem[1]]) - 1
                elif action == curses.KEY_RIGHT:
                    selecteditem[1] = (selecteditem[1] + 1) % 2

                    if selecteditem[0] > len(listall[selecteditem[1]]) - 1:
                        selecteditem[0] = len(listall[selecteditem[1]]) - 1
                elif action == "q" or action == curses.KEY_EXIT:
                    selecteditem[2] = 0
                    selection = selecteditem
                elif action == "\n":
                    selecteditem[2] = 1
                    selection = selecteditem
                elif action == "r":
                    selecteditem[2] = 2
                    selection = selecteditem
            except KeyboardInterrupt:
                sys.exit()
        return selection

    def add_pkey(self, screen):
        lenghlist = 2
        selecteditem = [0, -1]
        selection = [-1, -1, -1]
        valuesgiven = [""] * lenghlist
        valueskeysize = ["1024", "2048", "4096"]
        valueskeysizeselected = 2
        while max(selection) < 0:
            self.screen_window(screen, "~5", "~15", "~5", "~15",
                               curses.A_REVERSE + curses.color_pair(8))
            selected = [curses.A_REVERSE + curses.color_pair(8)
                        ] * (lenghlist + 1)
            selected[selecteditem[
                0]] = curses.A_REVERSE + curses.color_pair(204)
            screen.addstr(
                self.percentwin("50%", True) - 6,
                self.percentwin("50%", False) - 14,
                "Crear nova clau privada: ", selected[2])
            screen.addstr(
                self.percentwin("50%", True) + 3,
                self.percentwin("50%", False) - 14, "Tamany de la clau: " + "<"
                + valueskeysize[valueskeysizeselected] + ">", selected[1])
            screen.addstr(
                self.percentwin("50%", True),
                self.percentwin("50%", False) - 14, "Nom: " + valuesgiven[0],
                selected[0])
            screen.refresh()
            try:
                action = screen.get_wch()
                if action == curses.KEY_UP:
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist
                elif action == curses.KEY_DOWN:
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist
                elif action == curses.KEY_RIGHT:
                    if selecteditem[0] == 1:
                        valueskeysizeselected = (
                            valueskeysizeselected + 1) % len(valueskeysize)
                elif action == curses.KEY_LEFT:
                    if selecteditem[0] == 1:
                        valueskeysizeselected = (
                            valueskeysizeselected - 1) % len(valueskeysize)
                elif action == curses.KEY_EXIT or action == "\n" or action == "\x1b":
                    valuesgiven[1] = valueskeysize[valueskeysizeselected]
                    selection = selecteditem
                elif action == "\x7f":
                    if selecteditem[0] == 0:
                        valuesgiven[0] = valuesgiven[0][:-1]
                else:
                    if selecteditem[0] == 0:
                        valuesgiven[0] += action

            except KeyboardInterrupt:
                sys.exit()
        return valuesgiven

    def keyboardebugger(self, screen):
        text = ""
        q = str(ord("\n"))
        selection = [0, 0]
        a = True
        while a:
            screen.clear()
            screen.border()
            screen.addstr(2, 2, "%s: %s\n" % (repr(text), type(text)))
            screen.addstr(3, 2, q)
            screen.refresh()
            try:
                action = screen.get_wch()
                if action == "\n":
                    a = False
                else:
                    text = action
            except KeyboardInterrupt:
                sys.exit()
        return selection

    def solicit_ip_port_pwd(self, screen):
        lenghlist = 3
        selecteditem = 0
        done = False
        valuesgiven = [""] * (lenghlist + 1)
        while not done:
            self.screen_window(screen, "~5", "~15", "~6", "~15",
                               curses.A_REVERSE + curses.color_pair(8))
            selected = [curses.A_REVERSE + curses.color_pair(8)
                        ] * (lenghlist + 1)
            selected[selecteditem] = curses.A_REVERSE + curses.color_pair(204)
            screen.addstr(
                self.percentwin("50%", True) - 6,
                self.percentwin("50%", False) - 14, "Connexió a servidor: ",
                selected[3])
            screen.addstr(
                self.percentwin("50%", True) - 2,
                self.percentwin("50%", False) - 14, "IP: " + valuesgiven[0],
                selected[0])
            screen.addstr(
                self.percentwin("50%", True),
                self.percentwin("50%", False) - 14, "Port: " + valuesgiven[1],
                selected[1])
            screen.addstr(
                self.percentwin("50%", True) + 2,
                self.percentwin("50%", False) - 14,
                "Contrasenya: " + valuesgiven[2], selected[2])
            screen.refresh()
            try:
                action = screen.get_wch()
                if action == curses.KEY_UP:
                    selecteditem = (selecteditem - 1) % lenghlist
                elif action == curses.KEY_DOWN:
                    selecteditem = (selecteditem + 1) % lenghlist
                elif action == "\n":
                    done = True
                    valuesgiven[1] = int(valuesgiven[1])
                    valuesgiven[3] = True
                elif action == curses.KEY_EXIT or action == "\x1b":
                    done = True
                    valuesgiven[3] = False
                elif action == "\x7f":
                    valuesgiven[selecteditem] = valuesgiven[selecteditem][:-1]
                else:
                    valuesgiven[selecteditem] += str(action)
            except KeyboardInterrupt:
                sys.exit()
        return valuesgiven

    def client_screen(self, screen, args):
        screen.clear()
        client = Client_terminal(
            args[0], args[1], args[2], extra=[self.width - 2, self.height - 7])
        self.CLIENT_updateThread1 = True
        self.CLIENT_updateThread2 = True
        self.CLIENT_InProcessThread1 = False
        self.CLIENT_InProcessThread2 = False
        self.CLIENT_InProcessMAINThread = False
        self.CLIENT_rwitten_data = ""
        self.t1 = Thread(
            target=self.Threaded_client_screen_1, args=(screen, client))
        self.t1.daemon = True
        self.t1.start()
        self.t2 = Thread(target=self.Threaded_client_screen_2, args=(client, ))
        self.t2.daemon = True
        self.t2.start()
        temprefreix = 0
        try:
            while True:
                while self.CLIENT_InProcessThread1 and self.CLIENT_InProcessThread2:
                    temprefreix += 1
                self.CLIENT_InProcessMAINThread = True
                self.screen_window(screen, 0, 0, self.height - 2,
                                   self.width - 1,
                                   curses.color_pair(8) + curses.A_REVERSE)
                screen.addstr(2, 50, str(temprefreix))
                screen.addstr(self.height - 4, 0,
                              "├" + "─" * (self.width - 2) + "┤",
                              curses.color_pair(8) + curses.A_REVERSE)
                screen.addstr(2, 0, "├" + "─" * (self.width - 2) + "┤",
                              curses.color_pair(8) + curses.A_REVERSE)
                screen.addstr(
                    1, 1, "Connectat: " + str(client.ip) + ":" + str(
                        client.port) + " (" + client.State + ")",
                    curses.color_pair(8) + curses.A_REVERSE)
                screen.addstr(1, self.width - 10,
                              "Guests: " + str(len(client.people)),
                              curses.color_pair(8) + curses.A_REVERSE)
                x = 0
                for line in client.terminfo:
                    screen.addstr(3 + x, 1, line,
                                  curses.color_pair(8) + curses.A_REVERSE)
                    x += 1
                screen.addstr(self.height - 3, 1, self.CLIENT_rwitten_data,
                              curses.color_pair(8) + curses.A_REVERSE)
                screen.refresh()
                self.CLIENT_InProcessMAINThread = False
                if not self.t1.is_alive and not self.t2.is_alive:
                    return 0
                while not self.CLIENT_updateThread1 and not self.CLIENT_updateThread2:
                    pass
        except KeyboardInterrupt:
            sys.exit()

    def Threaded_client_screen_2(self, client):
        try:
            while True:
                time.sleep(1)
                while self.CLIENT_InProcessThread1 and self.CLIENT_InProcessMAINThread:
                    pass
                self.CLIENT_InProcessThread2 = True
                client.get_actions()
                self.CLIENT_updateThread2 = True
                self.CLIENT_InProcessThread2 = False
                if not self.t1.is_alive:
                    return 0
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit()

    def Threaded_client_screen_1(self, screen, client):
        try:
            while True:
                action = screen.get_wch()
                if action == "\n":
                    while self.CLIENT_InProcessThread2 and self.CLIENT_InProcessMAINThread:
                        pass
                    self.CLIENT_InProcessThread1 = True
                    client.send_message(self.CLIENT_rwitten_data)
                    client.process_incoming_data(client.recieve_message())
                    self.CLIENT_InProcessThread1 = False
                    self.CLIENT_updateThread1 = True
                    self.CLIENT_rwitten_data = ""
                elif action == "\x7f":
                    while self.CLIENT_InProcessThread2 and self.CLIENT_InProcessMAINThread:
                        pass
                    self.CLIENT_InProcessThread1 = True
                    if self.CLIENT_rwitten_data != "":
                        self.CLIENT_rwitten_data = self.CLIENT_rwitten_data[:
                                                                            -1]
                elif action == 259:
                    client.up()
                elif action == 258:
                    client.down()
                elif action == curses.KEY_EXIT:
                    self.CLIENT_updateThread1 = True
                    self.CLIENT_InProcessThread1 = False
                    return 0
                else:
                    self.CLIENT_rwitten_data += str(action)
            self.CLIENT_InProcessThread1 = False
            self.CLIENT_updateThread1 = True
            time.sleep(0.001)
        except KeyboardInterrupt:
            sys.exit()

    def config(self, screen, listkeys, name_selected):
        screen.clear()
        titol1 = "Clau Privada:"
        listoptions = [
            "(deprecated) Enviar clau pública",
            "(deprecated) Acceptar claus públiques (No preguntar)"
        ]
        listall = [listkeys, listoptions]
        listkeys.reverse()
        sizeinx = int(len(max(listkeys, key=len)))
        self.screen_window(screen, 0, 0, self.height - 2, self.width - 1,
                           curses.color_pair(5) + curses.A_REVERSE)
        minimum_window_1_size = 15
        if (minimum_window_1_size < sizeinx):
            real_window_1_size = sizeinx
        else:
            real_window_1_size = minimum_window_1_size
        self.screen_window(screen, 1, 1, 4 + len(listkeys),
                           real_window_1_size + 7,
                           curses.color_pair(8) + curses.A_REVERSE)
        #self.screen_window(screen, 1, sizeinx+9, 6, sizeinx+60, curses.color_pair(8)+curses.A_REVERSE)

        screen.addstr(1, 2, titol1, curses.A_REVERSE + curses.color_pair(8))
        selecteditem = [0, 0, -1]
        markedoptions = [name_selected, 1, 1]
        selection = [-1, -1, -1]
        while max(selection) < 0:
            lenghlist1 = len(listkeys)
            selected_key = [curses.A_REVERSE + curses.color_pair(8)
                            ] * lenghlist1
            selected_config = [curses.A_REVERSE + curses.color_pair(8)
                               ] * len(listoptions)
            if selecteditem[1] == 0:
                lenghlist = lenghlist1
                selected_key[selecteditem[
                    0]] = curses.A_REVERSE + curses.color_pair(204)
            elif selecteditem[1] == 1:
                lenghlist = len(listoptions)
                selected_config[selecteditem[
                    0]] = curses.A_REVERSE + curses.color_pair(204)
            #selected[0]
            x = 0
            for mail in listkeys:
                if x == markedoptions[0]:
                    selectionoptiontext = "[X]"
                else:
                    selectionoptiontext = "[ ]"
                screen.addstr(3 + x, 3, selectionoptiontext + " " + mail,
                              selected_key[x])
                x += 1
            x = 0
            for entrada in listoptions:
                if markedoptions[x + 1] == 1:
                    selectionoptiontext = "[X]"
                else:
                    selectionoptiontext = "[ ]"
                #screen.addstr(3+x,  sizeinx+10,selectionoptiontext + " " + entrada, selected_config[x])
                x += 1

            screen.refresh()
            try:
                action = screen.get_wch()
                if action == curses.KEY_UP:
                    selecteditem[0] = (selecteditem[0] - 1) % lenghlist
                elif action == curses.KEY_DOWN:
                    selecteditem[0] = (selecteditem[0] + 1) % lenghlist
                elif action == curses.KEY_LEFT:
                    pass
                    #selecteditem[1] = (selecteditem[1] - 1) % 2
                    #if selecteditem[0] > len(listall[selecteditem[1]])-1:
                elif action == curses.KEY_RIGHT:
                    pass
                    #selecteditem[1] = (selecteditem[1] + 1) % 2
                    #if selecteditem[0] > len(listall[selecteditem[1]])-1:
                elif action == "q" or action == curses.KEY_EXIT:
                    selecteditem[2] = 0
                    selection = markedoptions
                elif action == "\n":
                    selecteditem[2] = 1

                    selection = markedoptions
                elif action == " ":
                    if selecteditem[1] == 0:
                        markedoptions[0] = selecteditem[0]
                    else:
                        markedoptions[selecteditem[0] + 1] = (
                            markedoptions[selecteditem[0] + 1] + 1) % 2
            except KeyboardInterrupt:
                sys.exit()
        return selection

    def colordebugger(self, screen):
        checkvar1 = curses.has_colors()
        checkvar2 = curses.can_change_color()
        COLOR_NOW = curses.COLOR_PAIRS
        startwhitha0 = 0
        a = True
        while a:
            screen.clear()
            self.screen_window(screen, 0, 0, self.height - 2, self.width - 1,
                               curses.color_pair(5) + curses.A_REVERSE)
            screen.addstr(2, 2, str(checkvar1))
            screen.addstr(3, 2, str(checkvar2))
            screen.addstr(4, 2, str(curses.COLORS))
            screen.addstr(5, 2, str(curses.COLOR_PAIRS))
            starting = startwhitha0
            for y in range(0, 36):
                for x in range(0, 32):
                    screen.addstr(y + 10, 5 * x + 15, str(startwhitha0),
                                  curses.color_pair(startwhitha0))
                    startwhitha0 = 1 + startwhitha0 % COLOR_NOW
            startwhitha0 = starting
            try:
                action = screen.get_wch()
                if action == "\n":
                    a = False
                elif action == curses.KEY_UP:
                    startwhitha0 = (startwhitha0 - 32) % COLOR_NOW
                elif action == curses.KEY_DOWN:
                    startwhitha0 = (startwhitha0 + 32) % COLOR_NOW
                elif action == curses.KEY_RIGHT:
                    startwhitha0 = (startwhitha0 + 256) % COLOR_NOW
                elif action == curses.KEY_LEFT:
                    startwhitha0 = (startwhitha0 - 256) % COLOR_NOW
            except KeyboardInterrupt:
                sys.exit()

    def screen_window(self, screen, y0, x0, y1, x1, data=0):
        y0, y1 = self.complexwin(y0, y1, True)
        x0, x1 = self.complexwin(x0, x1, False)
        if (x0 > x1):
            tempx0 = x0
            x0 = x1
            x1 = tempx0
        if (y0 > y1):
            tempy0 = y0
            y0 = y1
            y1 = tempy0
        numslash = x1 - x0
        slash = "─" * numslash
        space = " " * numslash
        space = space[:-1]
        screen.addstr(y0, x0, slash, data)
        screen.addstr(y1, x0, slash, data)
        slash = "│"
        #la resta de linies
        for i in range(y0 + 1, y1):
            screen.addstr(i, x0, slash + space + slash, data)
        screen.addstr(y0, x0, "┌", data)
        screen.addstr(y0, x1, "┐", data)
        screen.addstr(y1, x0, "└", data)
        screen.addstr(y1, x1, "┘", data)
        return

    def complexwin(self, i0, i1, is_y=True):
        add = 0
        if (isinstance(i0, str)):
            if "~" in i0:
                i0 = i0.replace("~", "", 1)
                i0 = self.percentwin("50%", is_y) - int(
                    self.percentwin(i0, is_y)) - 1
            else:
                i0 = self.percentwin(i0, is_y)
                i0 = int(i0)
        if (isinstance(i1, str)):
            if "+" in i1:
                i1 = i1.replace("+", "", 1)
                add = i0
            if "~" in i1:
                i1 = i1.replace("~", "", 1)
                i1 = self.percentwin("50%", is_y) + int(
                    self.percentwin(i1, is_y))
            else:
                i1 = self.percentwin(i1, is_y)
        i1 = int(i1)
        i1 = i1 + add
        if i0 < 0:
            i1 -= (i0)
            i0 -= (i0)
        a = 0
        if is_y:
            a = self.height
        else:
            a = self.width
        if is_y:
            if i1 > a:
                i0 -= (i1 - a) + 2
                i1 -= (i1 - a) + 2
        else:
            if i1 > a:
                i0 -= (i1 - a) + 1
                i1 -= (i1 - a) + 1
        return i0, i1

    def percentwin(self, percent, is_y=True):
        if isinstance(percent, str):
            if "%" in percent:
                percent = int(percent.replace("%", "", 1))
                if (is_y):
                    percent = int(percent * self.height / 100)
                else:
                    percent = int(percent * self.width / 100)
        return percent
