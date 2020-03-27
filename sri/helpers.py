# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 00:58:46 2020

@author: djord
"""
from os import walk
from os.path import join
from os.path import splitext
import psutil
import platform

import sys
from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType

def dumparraytofile(array: [str], filepath: str):
    with open(filepath, "w", encoding="utf-8") as output:
        for line in array:
            print(line, file=output)
                    
def generateMachineInfo() -> str:
    strings = []
    strings.append("System: {0}".format(platform.platform()))
    strings.append("Processor: {0}".format(platform.processor()))
    strings.append("Ram: {0}".format(str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"))
    return '\n'.join(strings)

def getsize(obj):
    """sum size of object & members."""
    if isinstance(obj, BLACKLIST):
        raise TypeError('getsize() does not take argument of type: '+ str(type(obj)))
    seen_ids = set()
    size = 0
    objects = [obj]
    while objects:
        need_referents = []
        for obj in objects:
            if not isinstance(obj, BLACKLIST) and id(obj) not in seen_ids:
                seen_ids.add(id(obj))
                size += sys.getsizeof(obj)
                need_referents.append(obj)
        objects = get_referents(*need_referents)
    return size