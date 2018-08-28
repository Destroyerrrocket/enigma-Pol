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
    def __init__(self, GPGDir="~/.gnupgpol", ConfigDir="~/.config/EnigmaPol"):
        # hem serà útil per a un mac i per si en un futur decideixo portejar-lo a Windows
        self.OS = platform.system()
        # per al directori de treball.
        # probablement aquesta part es podrà configurar a alguna vanda més endavant

        self.GPGDir = GPGDir.replace("~", str(Path.home()), 1)
        self.ConfigDir = ConfigDir.replace("~", str(Path.home()), 1)

        # crearem el directori. GnuPG m'ha donat problemes si no la creem personalment
        if(not os.path.exists(self.GPGDir)):
            os.makedirs(self.GPGDir)
            subprocess.Popen(str("chmod 700 "+self.GPGDir).split())
            subprocess.Popen(str("chmod 600 " + self.GPGDir + "/*").split())
        if(not os.path.exists(self.ConfigDir)):
            os.makedirs(self.ConfigDir)

        self.gpg = gnupg.GPG(gnupghome=self.GPGDir)
        self.gpg.encoding = 'utf-8'
        # configuració predefinida
        self.sanity_check_for_users_data()


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
        if keys is not "":
            for i in range(0, len(keys)):
                fingerparsed = str(keys[i]["fingerprint"])
                finger.append(fingerparsed)
        if finger == []:
            pass
            #self.create_private_key()
            #finger = self.get_list_prkeys_fingerprint()
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
    def encrypt_message(self, message, fp):
        return self.gpg.encrypt(message, fp, always_trust=True)

    def decrypt_message(self, message):
        return self.gpg.decrypt(message)
    def export_key(self, fp):
        return self.gpg.export_keys(fp)
    def import_key(self, data):
        self.gpg.import_keys(data)

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

    def create_private_key(self, nom="default", lenghofkey="4096"):
        input_data = self.gpg.gen_key_input(key_type="RSA", key_length=lenghofkey, name_real=nom, name_comment="", name_email=str(nom+"@enigma.pol"))
        key = self.gpg.gen_key(input_data)
        pprint(key)
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

    def current_name(self):
        list_names = self.get_list_prkeys_name()
        list_fingr = self.get_list_prkeys_fingerprint()
        name = self.load_data("personal private key")
        id = 0
        for finger in list_fingr:
            if finger == name:
                break
            id += 1
        return list_names[id]

    def current_fp(self):
        list_names = self.get_list_prkeys_name()
        list_fingr = self.get_list_prkeys_fingerprint()
        name = self.load_data("personal private key")
        id = 0
        for finger in list_fingr:
            if finger == name:
                break
            id += 1
        return list_names[id]

    def dict_to_array(self, dictionary={}):
        array = dictionary.items()
        return array
    # espera data en format JSON
    def load_data(self, tag, category="config"):
        raw_datas = self.load_raw_data(category)
        for raw_data in raw_datas:
            return raw_data[tag]
    def save_data(self, data, tag, category="config"):
        original_data = self.load_raw_data()
        if original_data is not "":
            for configuration in original_data[category]:
                configuration[tag] = data
        else:
            original_data = {}
            original_data[category] = []
            original_data[category].append({
                tag : data
            })
        with open(self.ConfigDir+"/data.json", "w") as json_file:
                json.dump(original_data, json_file,
                          indent=2, ensure_ascii=False)
                json_file.close()

    def load_raw_data(self, category=""):
        try:
            with open(self.ConfigDir+"/data.json") as json_file:
                rawdata = json.load(json_file)
        except FileNotFoundError:
            return ""
        if category is not "":
            data = rawdata[category]
        else:
            data = rawdata
        json_file.close()
        return data

    def sanity_check_for_users_data(self, save_defaults=True):
        try:
            with open(self.ConfigDir + "/data.json") as json_file:
                json_file.close()
            return True
        except FileNotFoundError:
            if save_defaults:
                #self.save_data(0, "send public key")
                #self.save_data(0, "recieve public keys")
                fingerprints = self.get_list_prkeys_fingerprint()
                if fingerprints != []:
                    fingerprints.reverse()
                    fingerprint = fingerprints[0]
                    self.save_data(fingerprint, "personal private key")
            return False
