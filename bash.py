#!/bin/python3
# -*- coding: utf-8 -*-
# farà coses com ocupar-se de les crides a GPG.
import sys
import subprocess
import threading
import platform
import gnupg
from optparse import OptionParser
import os.path
import re
from pprint import pprint
class Bash(object):
    def __init__(self):
        self.OS = platform.system()
        # hem serà útil per a un mac i per si en un futur decideixo portejar-lo a Windows
    # No funciona. Sembla ser que no troba les claus de l'usuari. Pot ser que POPEN corri
    # el programa amb algun altre usuari? realment curiós.
    def get_list_pkeys_mail (self):
        gpg = gnupg.GPG(gnupghome='/home/pol/.gnupg')
        gpg.encoding = 'utf-8'
        keys = gpg.list_keys(True)
        mail = []
        for i in range(0, len(keys)):
            mailparsed = self.get_mails_on_text(str(keys[i]["uids"]))
            mail.append(mailparsed)
        pprint(mail)
        return mail
    def get_mails_on_text (self, text):
        pattern = re.compile("([a-z0-9!#$%&*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.))+[a-z0-9]"
                    "(?:[a-z0-9-]*[a-z0-9])?)|([a-z0-9!#$%&*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\sdot\s))+[a-z0-9]"
                    "(?:[a-z0-9-]*[a-z0-9])?)",re.S)
        email = re.findall(pattern,text)
        return (email[0][0])
