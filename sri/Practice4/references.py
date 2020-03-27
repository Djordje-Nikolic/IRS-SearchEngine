# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:28:35 2020

@author: djord
"""

class WordRef:
    def __init__(self):
        self.dict = {}
        self.counter = 1
        
    def addWord(self, word: str) -> int:
        hit = self.dict.get(word)
        if (hit is None):
            self.dict[word] = self.counter
            hit = self.counter
            self.counter += 1
        return hit     
    
    def addWords(self, words: [str]):
        result = []
        for word in words:
            result.append(self.addWord(word))
        return result
    
    def getWordID(self, word: str):
        return self.dict.get(word)
                      
    def getWordIDs(self, words: [str]):
        result = []
        for word in words:
            result.append(self.getWordID(word))
        return result
    
    def dumpInfo(self, filepath: str):
        with open(filepath, "w") as f:
            for key,value in self.dict.items():
                print("Word: {0} Id: {1}".format(key, value), file=f)

            
    
class FileRef:
    def __init__(self):
        self.dict = {}
        
    def addFile(self, filepath: str):
        hsh = hash(filepath)
        hit = self.dict.get(hsh)
        if (hit is None):
            self.dict[hsh] = filepath
        return hsh
    
    def getFilepath(self, hashvalue):
        return self.dict.get(hashvalue)
    
    def getfilecount(self):
        return len(self.dict)
    
    def dumpInfo(self, filepath: str):
        with open(filepath, "w") as f:
            for key,value in self.dict.items():
                print("Fileid: {0} Filepath: {1}".format(key, value), file=f)