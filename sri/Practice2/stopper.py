# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 03:20:10 2020

@author: djord
"""
from sri.Practice1.normalizer_tokenizer import Normalizer
import os

stopperpath = os.path.join(os.path.dirname(__file__), "stopwords.txt")

class Stopper:
    def __init__(self, metadataBefore = None, metadataAfter = None):
        self.metadataBefore = metadataBefore
        self.metadataAfter = metadataAfter
        self.stopwords = {}
        self.load(stopperpath)
        
    def load(self, filepath: str):
        normalizer = Normalizer()
        with open(filepath, "r") as file:
            for stopwordline in file:
                stopword = normalizer.normalize(stopwordline.replace('\n',""))
                
                #The counting here is unnecessary and is done only to show that 
                #there are multiple instances of the same stop words in the source 
                #material. This is especially evident when we remove the accents
                if (self.stopwords.get(stopword) is None):
                    self.stopwords[stopword] = 1
                else:
                    self.stopwords[stopword] += 1
            
    def removestops(self, array: [str]) -> [str]:
        result = []
        
        if (self.metadataBefore is not None):
            self.metadataBefore.countFile(array)
        
        for word in array:
            if (self.stopwords.get(word) is None):
                result.append(word)
                
        if (self.metadataAfter is not None):
            self.metadataAfter.countFile(result)
                
        return result
        
        
        