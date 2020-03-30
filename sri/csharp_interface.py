# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:07:07 2020

@author: djord
"""

import searchengine as se

searcheng = None

def load(configfilepath: str):
    try:
        global searcheng
        searcheng = se.SearchEngine(configfilepath, displayprocesstime = True)
    except Exception as ex:
        print("Error loading the search engine: {0}", ex)
        
def search(querystr: str, documentstoreturn: int = None, displayfullfilepath = False):
    try:
        searcheng.search(querystr, documentstoreturn = documentstoreturn, fullfilepath = displayfullfilepath)
    except Exception as ex:
        print("Error during search: {0}",ex)
        
        
#load("C:\\Users\\djord\\source\\repos\\IRS-SearchEngine\\sri\\config.txt")
#search("El olivar de Jaén.", documentstoreturn = 10)