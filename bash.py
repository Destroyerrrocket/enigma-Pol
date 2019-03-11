#!/bin/python3
# -*- coding: utf-8 -*-
# farà coses com ocupar-se de les crides a GPG.
import sys
import os
#import errno
import subprocess
import platform
import gnupg
import re
from pprint import pprint
from pathlib import Path
import json


class Bash(object):
    def __init__(self, GPGDir="~/.gnupgpol", ConfigDir="~/.config/EnigmaPol"):
        self.OS = platform.system()
        pprint("Current OS: " + self.OS)

        self.GPGDir = GPGDir.replace("~", str(Path.home()), 1)
        self.ConfigDir = ConfigDir.replace("~", str(Path.home()), 1)

        if (not os.path.exists(self.GPGDir)):
            os.makedirs(self.GPGDir)
            subprocess.Popen(str("chmod 700 " + self.GPGDir).split())
            subprocess.Popen(str("chmod 600 " + self.GPGDir + "/*").split())
        if (not os.path.exists(self.ConfigDir)):
            os.makedirs(self.ConfigDir)
        if (self.OS == "Linux"):
            self.gpg = gnupg.GPG(
                homedir=self.GPGDir,
                keyring='pubring.gpg',
                secring='trustdb.gpg')
        else:
            pprint(
                "No soportem " + self.OS +
                "! Instal·la un sistema operatiu Linux per a utilitzar Enigma-Pol"
            )
            sys.exit(0)

        self.gpg.encoding = 'utf-8'
        self.sanity_check_for_users_data()

    def get_list_prkeys_mail(self):
        keys = self.gpg.list_keys(True)
        mail = []
        for i in range(0, len(keys)):
            mailparsed = self.get_mails_on_text(str(keys[i]["uids"]))
            mail.append(mailparsed)
        return mail

    def get_list_pukeys_mail(self):
        keys = self.gpg.list_keys(False)
        mail = []
        for i in range(0, len(keys)):
            mailparsed = self.get_mails_on_text(str(keys[i]["uids"]))
            mail.append(mailparsed)
        return mail

    def get_list_prkeys_name(self):
        keys = self.gpg.list_keys(True)
        name = []
        for i in range(0, len(keys)):
            nameparsed = self.get_names_on_text(str(keys[i]["uids"]))
            name.append(nameparsed)
        return name

    def get_list_pukeys_name(self):
        keys = self.gpg.list_keys()
        name = []
        for i in range(0, len(keys)):
            nameparsed = self.get_names_on_text(str(keys[i]["uids"]))
            name.append(nameparsed)
        return name

    def get_list_prkeys_fingerprint(self):
        keys = self.gpg.list_keys(True)
        finger = []
        if keys is not "":
            for i in range(0, len(keys)):
                fingerparsed = str(keys[i]["fingerprint"])
                finger.append(fingerparsed)
        if finger == []:
            pass
            #finger = self.get_list_prkeys_fingerprint()
        return finger

    def get_list_pukeys_fingerprint(self):
        keys = self.gpg.list_keys(False)
        finger = []
        for i in range(0, len(keys)):
            fingerparsed = str(keys[i]["fingerprint"])
            finger.append(fingerparsed)
        return finger

    def get_list_prkeys_all(self):
        keys = self.gpg.list_keys(True)
        return keys

    def get_list_pukeys_all(self):
        keys = self.gpg.list_keys()
        return keys

    def encrypt_message(self, message, fp):
        return self.gpg.encrypt(
            message,
            fp,
            default_key=self.current_fp(),
            always_trust=True,
            throw_keyids=True,
        )

    def decrypt_message(self, message):
        decrypted = ""
        try:
            decrypted = self.gpg.decrypt(message, always_trust=True)
        except:
            pass
        return decrypted

    def export_key(self, fp):
        return self.gpg.export_keys(fp)

    def import_key(self, data):
        self.gpg.import_keys(data)

    def get_names_on_text(self, text1):
        pattern1 = re.compile(" \<[^)]*\>|\([^)]*\)", re.S)
        text2 = re.sub(pattern1, "", text1)
        name = text2[2:-2]
        return name

    def get_mails_on_text(self, text):
        # patró de regex per a trobar correus.
        pattern = re.compile(
            "([a-z0-9!#$%&*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
            "{|}~-]+)*(@)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.))+[a-z0-9]"
            "(?:[a-z0-9-]*[a-z0-9])?)|([a-z0-9!#$%&*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
            "{|}~-]+)*(\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\sdot\s))+[a-z0-9]"
            "(?:[a-z0-9-]*[a-z0-9])?)", re.S)
        email = re.findall(pattern, text)
        return (email[0][0])

    def create_private_key(self, nom="default", lenghofkey="4096"):
        input_data = self.gpg.gen_key_input(
            key_type="RSA",
            key_length=int(lenghofkey),
            name_real=nom,
            name_email=str(nom + "@enigma.pol"))
        key = self.gpg.gen_key(input_data)
        return key

    def remove_prkey(self, fingerprint="", id=-1):
        delete_private_key = "gpg --batch --homedir " + self.GPGDir + " --delete-secret-key "
        if fingerprint == "" and id == -1:
            return
        elif id != -1:
            fingerprints = self.get_list_prkeys_fingerprint()
            fingerprints.reverse()
            fingerprint = fingerprints[id]
        if fingerprint != "" and (isinstance(fingerprint, str)):
            process = subprocess.Popen(
                str(delete_private_key + fingerprint).split(),
                stdout=subprocess.PIPE)
            output, error = process.communicate()
        return

    def remove_pukey(self, fingerprint="", id=-1):
        delete_public_key = "gpg --batch --homedir " + self.GPGDir + " --delete-key "
        if fingerprint == "" and id == -1:
            return
        elif id != -1:
            fingerprints = self.get_list_pukeys_fingerprint()
            fingerprints.reverse()
            fingerprint = fingerprints[id]
        if fingerprint != "" and (isinstance(fingerprint, str)):
            self.remove_prkey(fingerprint=fingerprint)
            process = subprocess.Popen(
                str(delete_public_key + fingerprint).split(),
                stdout=subprocess.PIPE)
            output, error = process.communicate()
        return

    def current_name(self):
        list_names = self.get_list_prkeys_name()
        list_fingr = self.get_list_prkeys_fingerprint()
        name = self.load_data("personal private key")
        id = list_fingr.index(name)
        return list_names[id]

    def current_fp(self):
        return self.load_data("personal private key")

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
            original_data[category].append({tag: data})
        with open(self.ConfigDir + "/data.json", "w") as json_file:
            json.dump(original_data, json_file, indent=2, ensure_ascii=False)
            json_file.close()

    def load_raw_data(self, category=""):
        try:
            with open(self.ConfigDir + "/data.json") as json_file:
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
                fingerprints = self.get_list_prkeys_fingerprint()
                if fingerprints != []:
                    fingerprints.reverse()
                    fingerprint = fingerprints[0]
                    self.save_data(fingerprint, "personal private key")
            return False
