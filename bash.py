#!/bin/python3
# -*- coding: utf-8 -*-
# farà coses com ocupar-se de les crides a GPG.
import sys
import subprocess
import threading
import platform
class Bash(object):
    def __init__(self):
        # hem serà útil per a un mac i per si en un futur decideixo portejar-lo a Windows
        self.OS = platform.system()
    # No funciona. Sembla ser que no troba les claus de l'usuari. Pot ser que POPEN corri
    # el programa amb algun altre usuari? realment curiós.
    def get_list_pkeys (self):
        bashCommand = "gpg --list-secret-keys --keyid-format short | grep sec | cut -d' ' -f 4; touch ~/wtf"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return output;
