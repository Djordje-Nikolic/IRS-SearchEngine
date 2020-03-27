# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 20:53:28 2020

@author: djord
"""
from bs4 import BeautifulSoup
import bs4

class HtmlFilter:
    def __init__(self, filepath = None):
        if (filepath is not None):
            self.setFilepath(filepath)
        
    def setFilepath(self, filepath):
        self.filepath = filepath
        self.content = []
        self.serializedContent = ""
        
    def addToContent(self, text: str):
        # ignore empty text
        if text:
            self.content.append(text)
        
    def filterContent(self):
        with open(self.filepath, "r", encoding="utf8") as file:
            soup = BeautifulSoup(file, features="lxml")
            
            #Add title to content
            titletag = soup.title
            if (titletag is not None):
                self.addToContent(titletag.text)
                           
            #Add text from all children of the bodytag
            bodytag = soup.body
            if (bodytag is not None):
                for descendant in bodytag.descendants:
                    if isinstance(descendant, bs4.element.NavigableString) and not isinstance(descendant, bs4.element.Comment) and descendant.parent.name != 'script':
                        text = descendant.strip()
                        self.addToContent(text)
    
    def getContent(self):
        if (self.serializedContent == ""):
            self.serializedContent = ' '.join(self.content)
        return self.serializedContent