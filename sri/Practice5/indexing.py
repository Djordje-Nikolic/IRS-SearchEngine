# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 22:47:33 2020

@author: djord
"""

import sri.Practice4.references as refs  
import math
from sri.helpers import insertinsorted

class WFData:
    def __init__(self):
        self.freq = 0
        self.tf = -1
        self.w = -1
        self.wn = -1
        
    def increment(self):
        self.freq += 1
        
    def calculateTF(self, maxfreq):
        self.tf = self.freq / maxfreq
        return self.tf
    
    def calculateW(self, IDF):
        self.w = self.tf * IDF
        return self.w
    
    def calculateWn(self, norm):
        self.wn = self.w / norm
        return self.wn
    
    def __repr__(self):
        return "Freq: {0} Tf: {1} W: {2} Wn: {3}".format(self.freq, self.tf, self.w, self.wn)

class WordInfo:
    def __init__(self):
        self.IDF = -1
        self.filedict = {}
        
    def addfile(self, fileid):
        hit = self.filedict.get(fileid)
        if (hit is None):
            hit = WFData()
            self.filedict[fileid] = hit
        hit.increment()
        
    def getwfdata(self, fileid):
        return self.filedict.get(fileid)
    
    def setIDF(self, totalfilecount):
        res1 = (totalfilecount + 1) / (len(self.filedict) + 1)
        self.IDF = math.log2(res1) + 1
    
    def calcWs(self):
        for _, wfdata in self.filedict.items():
            wfdata.calculateW(self.IDF)
    
    def __repr__(self):
        pairs = []
        for key,value in self.filedict.items():
            pairs.append("FileID: {0} Data: {1}".format(key, value))
        pairs.append("IDF: {0}".format(self.IDF))
        return '\n'.join(pairs)
    
    # Add something for self.sqrtSumOfSqrWordWeights calculating and setting

class IndexingData:
    def __init__(self, fileref: refs.FileRef = None):
        self.maindict = {}
        self.norms = None
        self.fileref = fileref
        
    def setFileRef(self, fileref: refs.FileRef):
        self.fileref = fileref
        
    def countWord(self, wordid, fileid):
        hit = self.maindict.get(wordid)
        if (hit is None):
            hit = WordInfo()
            self.maindict[wordid] = hit
        hit.addfile(fileid)
    
    def getwordinfo(self, wordid):
        return self.maindict.get(wordid)
    
    def getwordidf(self, wordid):
        hit = self.maindict.get(wordid)
        if (hit is not None):
            return hit.IDF
        else:
            filecount = self.fileref.getfilecount()
            res1 = (filecount + 1) / 1
            return math.log2(res1) + 1
    
    def __repr__(self):
        filedata = []
        for key,value in self.maindict.items():          
            filedata.append("WordID: {0} WordData: \n{1}".format(key, value))
        return '\n'.join(filedata)
    
    def dumpInfo(self, filepath: str):
        with open(filepath, "w") as f:
            print(self, file=f)
            
    def calculateFull(self):
        self.calcTFs()
        self.calcIDFs()
        self.calcWs()
        self.calcWns()
            
    ### <LEGACY CODE>
    def calcFileMaxFreq(self, fileid) -> {}:
        currmax = 0
        for _, worddata in self.maindict.items():
            wfdata = worddata.getwfdata(fileid)
            if (wfdata is not None):
                if (wfdata.freq > currmax):
                    currmax = wfdata.freq
        return currmax
    ### <\LEGACY CODE>
    
    def calcFileMaxFreqs(self):
        result = {}
        for _, worddata in self.maindict.items():
            for fileid, wfdata in worddata.filedict.items():
                hit = result.get(fileid)
                if (hit is None):
                    hit = wfdata.freq
                else:
                    if (wfdata.freq > hit):
                        hit = wfdata.freq
                result[fileid] = hit
        return result

    def calcTFs(self):
#        filemaxfreqs = {}
#        for fileid,_ in fileref.dict.items():
#            filemaxfreq = self.calcFileMaxFreq(fileid)
#            filemaxfreqs[fileid] = filemaxfreq
        filemaxfreqs = self.calcFileMaxFreqs()
            
        for _, worddata in self.maindict.items():
            for fileid, wfdata in worddata.filedict.items():
                wfdata.calculateTF(filemaxfreqs[fileid])
                
    def calcIDFs(self):
        filecount = self.fileref.getfilecount()
        for _, worddata in self.maindict.items():
            worddata.setIDF(filecount)
            
    def calcWs(self):
        for _, worddata in self.maindict.items():
            worddata.calcWs()
            
    def calcNorms(self, recalc = False):
        if (self.norms is not None and not recalc):
            return self.norms
        
        result = {}
        for _, worddata in self.maindict.items():
            for fileid, wfdata in worddata.filedict.items():
                if (fileid not in result):
                    result[fileid] = 0
                result[fileid] += math.pow(wfdata.w, 2)
        for fileid, value in result.items():
            result[fileid] = math.sqrt(value)
            
        self.norms = result    
        return self.norms
        
    def calcWns(self, recalcnorms = False):
        norms = self.calcNorms(recalc = recalcnorms)
        
        for _, worddata in self.maindict.items():
            for fileid, wfdata in worddata.filedict.items():
                wfdata.calculateWn(norms[fileid])
                
    def getMostCommonWords(self, count: int = 5):
        result = {}
        
        for wordid, worddata in self.maindict.items():
            for fileid, wfdata in worddata.filedict.items():
                hit = result.get(fileid)
                if hit is None:
                    hit = []
                
                commonTuple = (wordid, wfdata.freq)
                insertinsorted(hit, commonTuple, lambda x: x[1], desc=True)
                
                hit = hit[0:count]
                result[fileid] = hit
                
        return result
        