# -*- coding: utf-8 -*-
'''
Created on 2019/07/10

@author: Kein-Chan
'''
##file load 
import json

class File:
    def __init__(self, jsonfile):
        self.jsonfile = jsonfile

    def load_file(self):
        try:
            f = open(self.jsonfile, 'r')
            loadFile = json.load(f)
            f.close()
            return loadFile

        except IOError:
            print("IOError occurred")

    def write_jsonfile(self, mode, aboutVnf):
        try:

            f = open(self.jsonfile, mode)
            # aboutVnf2 = json.dumps(aboutVnf)
            #json.dump(aboutVnf, f, indent=4, sort_keys=True, ensure_ascii=False)
            json.dump(aboutVnf, f, indent=4, ensure_ascii=False)
            f.close()

        except IOError:
            print("IOError occurred")

    def wirte_file(self, mode, aboutVnf):
        try:
            f = open(self.jsonfile, mode)
            f.write(aboutVnf + "\n")
            f.close()
        except IOError:
            print("IOError occurred")
