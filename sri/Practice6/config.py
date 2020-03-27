# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 04:18:47 2020

@author: djord
"""

def parse(configpath: str):
    structuresfolderpath = None
    collectionfolderpath = None
    with open(configpath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '').strip()
            res = line.find("structures=")
            if res != -1:
                structuresfolderpath = line[res + len("structures="):]
                continue
            res = line.find("collection=")
            if res != -1:
                collectionfolderpath = line[res + len("collection="):]
                continue
            
    return structuresfolderpath, collectionfolderpath
