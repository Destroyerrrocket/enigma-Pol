#!/bin/python3
# -*- coding: utf-8 -*-
# farà coses com ocupar-se de les crides a GPG.
import sys
import os
import errno
import subprocess
import threading
import platform
import gnupg
from optparse import OptionParser
from pathlib import Path
import re
from pprint import pprint
class Bash(object):
    def __init__(self):
        # hem serà útil per a un mac i per si en un futur decideixo portejar-lo a Windows
        self.OS = platform.system()
        # per al directori de treball.
        # probablement aquesta part es podrà configurar a alguna vanda més endavant
        self.Dir = str(str(Path.home())+"/.gnupgpol")
        # crearem el directori. GnuPG m'ha donat problemes si no la creem personalment
        if(not os.path.exists(self.Dir)):
            os.makedirs(self.Dir)
        self.gpg = gnupg.GPG(gnupghome=self.Dir)
        self.gpg.encoding = 'utf-8'
    # ja funciona. LLista totes les claus del directori
    def get_list_pkeys_mail (self):
        # definim la carpeta arrel. S'ha decidit usar una pròpia.
        keys = self.gpg.list_keys(True)
        # variable que contindrà els mails
        mail = []
        # màgia iterativa per a aconseguir els mails
        for i in range(0, len(keys)):
            mailparsed = self.get_mails_on_text(str(keys[i]["uids"]))
            mail.append(mailparsed)
        pprint(mail)
        return mail
    def get_list_pkeys_name (self):
        # definim la carpeta arrel. S'ha decidit usar una pròpia.

        keys = self.gpg.list_keys(True)
        pprint(keys)
        # variable que contindrà els mails
        name = []
        # màgia iterativa per a aconseguir els mails
        for i in range(0, len(keys)):
            nameparsed = self.get_names_on_text(str(keys[i]["uids"]))
            name.append(nameparsed)
        pprint(name)
        return name
    # Aquesta part conté la màgia iterativa.
    def get_names_on_text (self, text):
        pattern = re.compile("\([^)]*\) \<[^)]*\>",re.S)
        name = re.sub(pattern,"",text)
        return name

    def get_mails_on_text (self, text):
        # patró de regex per a trobar correus. per al que ens interessa està una mica massa desenvolupat,
        # però funciona. I això és el més important al final del dia
        pattern = re.compile("([a-z0-9!#$%&*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.))+[a-z0-9]"
                    "(?:[a-z0-9-]*[a-z0-9])?)|([a-z0-9!#$%&*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\sdot\s))+[a-z0-9]"
                    "(?:[a-z0-9-]*[a-z0-9])?)",re.S)
        # apliquem la búsqueda
        email = re.findall(pattern,text)
        # retornem la part resultant que ens interessa. Sempre és la primera, així que no hi ha problema
        return (email[0][0])
    # en desenvolupament
    def create_private_key (self, nom, lenghofkey):
        input_data = self.gpg.gen_key_input(key_type="RSA", key_length=lenghofkey, name_real=nom, name_comment="", name_email=str(nom+"@enigma.pol"))
        key = self.gpg.gen_key(input_data)
        return key;