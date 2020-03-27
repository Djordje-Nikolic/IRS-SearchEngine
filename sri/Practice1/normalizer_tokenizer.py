# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 00:07:29 2020

@author: djord
"""
import helpers 
import re

class Normalizer:
    def __init__(self):
        self.accentmap = { u"á" : "a", 
                           u"é" : "e", 
                           u"í" : "i",
                           u"ó" : "o",
                           u"ú" : "u",
                           u"ñ" : "n",
                           u"ü" : "u" }
        self.forbiddencharpattern =  "[^a-z0-9\s\_\-\n]"
        
    def getnonaccented(self, letter):
        nonaccented = self.accentmap.get(letter)
        if (nonaccented is None):
            nonaccented = letter
        return nonaccented
    
    def isforbidden(self, letter) -> bool:
        result = re.search(self.forbiddencharpattern, letter, re.I)
        if result is not None:
            return True
        else:
            return False
    
    def normalize(self, text: str) -> str:
        normalizedtextarr = []
        for letter in text:
            normalizedletter = self.getnonaccented(letter.lower())
            if not self.isforbidden(normalizedletter):
                normalizedtextarr.append(normalizedletter)
                
        return ''.join(normalizedtextarr)
    
class Tokenizer:
    def __init__(self):
        #UBACI OSTALE DOZVOLJENE KARAKTERE?
        self.tokenizepattern = "[^\s\W\_\-]+(?:'[^\s\W\_\-])?"
        
    def tokenize(self, text: str) -> [str]:
        return re.findall(self.tokenizepattern, text)
    
    def tokenizetofile(self, text: str, filepath: str):
        helpers.dumparraytofile(self.tokenize(text), filepath)
    
def normalize_tokenize(text: str, normalizer = Normalizer(), tokenizer = Tokenizer(), metadata = None) -> [str]:
    normalizedtext = normalizer.normalize(text)
    tokens = tokenizer.tokenize(normalizedtext)
    
    if metadata is not None:
        metadata.countFile(len(tokens))
    
    return tokens

def normalize_tokenizetofile(text: str, filepath: str, normalizer = Normalizer(), tokenizer = Tokenizer(), metadata = None):
    tokens = normalize_tokenize(text, normalizer, tokenizer, metadata=metadata)
    helpers.dumparraytofile(tokens, filepath)
    
def readtokens_fromfile(filepath: str):
    tokens = []
    with open(filepath, "r") as file:
        for line in file:
            tokens.append(line.replace('\n', ''))
    return tokens
    