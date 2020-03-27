# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 01:06:44 2020

@author: djord
"""
import sys
import os

if (os.path.abspath(os.path.dirname(__file__)) not in sys.path):
    sys.path.append(os.path.abspath("..")) 
    sys.path.append(os.path.abspath(os.path.dirname(__file__)))
    sys.path.append(os.path.abspath(".\Practice1"))
    sys.path.append(os.path.abspath(".\Practice2"))
    sys.path.append(os.path.abspath(".\Practice3"))
    sys.path.append(os.path.abspath(".\Practice4"))
    sys.path.append(os.path.abspath(".\Practice5"))
    sys.path.append(os.path.abspath(".\Practice6"))
    sys.path.append(os.path.abspath(".\Practice7"))
    print('\n'.join(sys.path))