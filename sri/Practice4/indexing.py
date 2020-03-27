# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:47:33 2020

@author: djord
"""

class WordInfo:
    def __init__(self):
        self.filedict = {}
        
    def addfile(self, fileid):
        hit = self.filedict.get(fileid)
        if (hit is None):
            self.filedict[fileid] = 1
        else:
            self.filedict[fileid] += 1
        
    def getwfdata(self, fileid):
        return self.filedict.get(fileid)
    
    def __repr__(self):
        pairs = []
        for key,value in self.filedict.items():
            pairs.append("FileID: {0} Freq: {1}".format(key, value))
        return '\n'.join(pairs)

class IndexingData:
    def __init__(self):
        self.maindict = {}
        
    def countWord(self, wordid, fileid):
        hit = self.maindict.get(wordid)
        if (hit is None):
            hit = WordInfo()
            self.maindict[wordid] = hit
        hit.addfile(fileid)
    
    def getwordinfo(self, wordid):
        return self.maindict.get(wordid)
    
    def __repr__(self):
        filedata = []
        for key,value in self.maindict.items():          
            filedata.append("WordID: {0} WordData: \n{1}".format(key, value))
        return '\n'.join(filedata)
    
    def dumpInfo(self, filepath: str):
        with open(filepath, "w") as f:
            print(self, file=f)
    
    
        