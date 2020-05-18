# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 00:58:46 2020

@author: djord
"""
from os import walk
from os.path import join
from os.path import splitext
from typing import Callable
import psutil
import platform

import sys
from types import ModuleType, FunctionType
from gc import get_referents

# Custom objects know their class.
# Function objects seem to know way too much, including modules.
# Exclude modules as well.
BLACKLIST = type, ModuleType, FunctionType

def insertinsorted(array: [], newVal, key: Callable, desc: bool = True):
    index = binSearch(array, key(newVal), key, desc)
    array.insert(index, newVal)
    return array
    
def binSearch(array: [], value, key: Callable, desc: bool = True):
    if len(array) == 0:
        return 0
    
    left, right = 0, len(array) - 1

    while left < right:
        middle = (left + right) // 2
        middle_element = key(array[middle])

        if middle_element == value:
            return middle
                
        if not desc:         
            if middle_element < value:
                left = middle + 1
            elif middle_element > value:
                right = middle - 1
        else:
            if middle_element < value:
                right = middle - 1
            elif middle_element > value:
                left = middle + 1
        
    if left == right:
        middle = left
        middle_element = key(array[middle])
        
        if middle_element == value:
            return middle
        
        if not desc:         
            if middle_element < value:
                return middle + 1
            elif middle_element > value:
                return middle
        else:
            if middle_element < value:
                return middle
            elif middle_element > value:
                return middle + 1
    else:
        return middle

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

#lista = []
#insertinsorted(lista, ("kurac", 6), lambda x: x[1], desc=True)
#insertinsorted(lista, ("kurac", 4), lambda x: x[1], desc=True)
#insertinsorted(lista, ("kurac", 1), lambda x: x[1], desc=True)
#insertinsorted(lista, ("kurac", 2), lambda x: x[1], desc=True)
#insertinsorted(lista, ("kurac", 4), lambda x: x[1], desc=True)
#insertinsorted(lista, ("kurac", 4), lambda x: x[1], desc=True)
#insertinsorted(lista, ("kurac", 9), lambda x: x[1], desc=True)
#insertinsorted(lista, ("kurac", -1), lambda x: x[1], desc=True)
#print(lista)
#
#lista = []
#insertinsorted(lista, ("kurac", 6), lambda x: x[1], desc=False)
#insertinsorted(lista, ("kurac", 4), lambda x: x[1], desc=False)
#insertinsorted(lista, ("kurac", 1), lambda x: x[1], desc=False)
#insertinsorted(lista, ("kurac", 2), lambda x: x[1], desc=False)
#insertinsorted(lista, ("kurac", 4), lambda x: x[1], desc=False)
#insertinsorted(lista, ("kurac", 4), lambda x: x[1], desc=False)
#insertinsorted(lista, ("kurac", 9), lambda x: x[1], desc=False)
#insertinsorted(lista, ("kurac", -1), lambda x: x[1], desc=False)
#print(lista)