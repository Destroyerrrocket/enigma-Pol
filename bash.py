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
import json
class Bash(object):
    def __init__(self):
        # hem serà útil per a un mac i per si en un futur decideixo portejar-lo a Windows
        self.OS = platform.system()
        # per al directori de treball.
        # probablement aquesta part es podrà configurar a alguna vanda més endavant
        self.GPGDir = str(Path.home()) + "/.gnupgpol"
        self.ConfigDir = str(Path.home()) + "/.config/EnigmaPol"
        # crearem el directori. GnuPG m'ha donat problemes si no la creem personalment
        if(not os.path.exists(self.GPGDir)):
            os.makedirs(self.GPGDir)
            subprocess.Popen(str("chmod 700 "+self.GPGDir).split())
            subprocess.Popen(str("chmod 600 " + self.GPGDir + "/*").split())
        if(not os.path.exists(self.ConfigDir)):
            os.makedirs(self.ConfigDir)
        
        self.gpg = gnupg.GPG(gnupghome=self.GPGDir)
        self.gpg.encoding = 'utf-8'
    # ja funciona. LLista totes les claus del directori
    def get_list_prkeys_mail (self):
        keys = self.gpg.list_keys(True)
        # variable que contindrà els mails
        mail = []
        # màgia iterativa per a aconseguir els mails
        for i in range(0, len(keys)):
            mailparsed = self.get_mails_on_text(str(keys[i]["uids"]))
            mail.append(mailparsed)
        return mail
    def get_list_pukeys_mail (self):
        keys = self.gpg.list_keys(False)
        # variable que contindrà els mails
        mail = []
        # màgia iterativa per a aconseguir els mails
        for i in range(0, len(keys)):
            mailparsed = self.get_mails_on_text(str(keys[i]["uids"]))
            mail.append(mailparsed)
        return mail
    def get_list_prkeys_name (self):
        keys = self.gpg.list_keys(True)
        # variable que contindrà els mails
        name = []
        # màgia iterativa per a aconseguir els mails
        for i in range(0, len(keys)):
            nameparsed = self.get_names_on_text(str(keys[i]["uids"]))
            name.append(nameparsed)
        return name
    def get_list_pukeys_name (self):
        keys = self.gpg.list_keys()
        # variable que contindrà els mails
        name = []
        # màgia iterativa per a aconseguir els mails
        for i in range(0, len(keys)):
            nameparsed = self.get_names_on_text(str(keys[i]["uids"]))
            name.append(nameparsed)
        return name
    def get_list_prkeys_fingerprint (self):
        keys = self.gpg.list_keys(True)
        # variable que contindrà els mails
        finger = []
        # màgia iterativa per a aconseguir els mails
        for i in range(0, len(keys)):
            fingerparsed = str(keys[i]["fingerprint"])
            finger.append(fingerparsed)
        return finger
    def get_list_pukeys_fingerprint (self):
        keys = self.gpg.list_keys(False)
        # variable que contindrà els mails
        finger = []
        # màgia iterativa per a aconseguir els mails
        for i in range(0, len(keys)):
            fingerparsed = str(keys[i]["fingerprint"])
            finger.append(fingerparsed)
        return finger
    def get_list_prkeys_all (self):
        keys = self.gpg.list_keys(True)
        # variable que contindrà els mails
        return keys
    def get_list_pukeys_all (self):
        keys = self.gpg.list_keys()
        # variable que contindrà els mails
        return keys
    # Aquesta part conté la màgia iterativa.
    def get_names_on_text (self, text1):
        pattern1 = re.compile(" \<[^)]*\>|\([^)]*\)",re.S)
        text2 = re.sub(pattern1,"",text1)
        name = text2[2:-2]
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
        return key
    def remove_prkey (self, fingerprint="", id=-1):
        delete_private_key = "gpg --batch --homedir "+self.GPGDir+" --delete-secret-key "
        if fingerprint == "" and id == -1:
            return
        elif id != -1:
            fingerprints = self.get_list_prkeys_fingerprint()
            fingerprints.reverse()
            fingerprint = fingerprints[id]
        if fingerprint != "" and (isinstance(fingerprint,str)):
            process = subprocess.Popen(str(delete_private_key + fingerprint).split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        return
    def remove_pukey (self, fingerprint="", id=-1):
        delete_public_key  = "gpg --batch --homedir "+self.GPGDir+" --delete-key "
        if fingerprint == "" and id == -1:
            return
        elif id != -1:
            fingerprints = self.get_list_pukeys_fingerprint()
            fingerprints.reverse()
            fingerprint = fingerprints[id]
        if fingerprint != "" and (isinstance(fingerprint,str)):
            self.remove_prkey(fingerprint=fingerprint)
            process = subprocess.Popen(str(delete_public_key + fingerprint).split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        return
    # espera data en format JSON
    # TODO: Cambiem com treballem: farem que Bash s'ocupi d'administrar la configuració
    def save_data(self, data):
        with open(self.ConfigDir+'/data.txt', 'w') as outfile:
            json.dump(data, outfile)

    
