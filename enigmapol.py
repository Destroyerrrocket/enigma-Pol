#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import curses
import threading
import locale
import json
from pprint import pprint
from drawer import Drawer
from bash import Bash


class EnigmaPol(object):
    def make_choice(self):
        KeepGoing = True
        while KeepGoing:
            choice = drawer.main_menu(screen)[0]
            if choice == 0:
                self.client_administrator()
            elif choice == 1:
                self.configuration()
            elif choice == 2:
                self.gpg_administrator()
            elif choice == 3:
                KeepGoing = False

    def gpg_administrator(self):
        while True:
            is_list_empty = [False, False]
            list1 = bash.get_list_prkeys_name()
            list2 = bash.get_list_pukeys_name()
            if len(list2) < 1:
                list2.append("--Buit--")
                is_list_empty[1] = True
            finalist = [list1, list2]
            choice = drawer.list_pkeys(screen, finalist)
            if choice[2] == 0:
                return
            elif choice == [0, 0, 1]:
                choice2 = drawer.add_pkey(screen)
                if choice2[0] != "":
                    bash.create_private_key(choice2[0], choice2[1])
            if choice[2] == 2:
                if choice[1] == 1 and is_list_empty[1] == False:
                    bash.remove_pukey(id=choice[0])
                elif choice[1] == 0 and is_list_empty[1] == False:
                    choice[0] -= 1
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
        config = drawer.config(screen, list1, name_selected_index)
        fingerprints = bash.get_list_prkeys_fingerprint()
        fingerprints.reverse()
        fingerprint = fingerprints[config[0]]
        bash.save_data(fingerprint, "personal private key")

    def client_administrator(self):
        choice = drawer.solicit_ip_port_pwd(screen)
        if choice[3] == True:
            drawer.client_screen(screen, [choice[0], choice[1], choice[2]])


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
    enigmapol.make_choice()


if __name__ == "__main__":
    curses.wrapper(setup_enigmapol)
    sys.exit(0)
