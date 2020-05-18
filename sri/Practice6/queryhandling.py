# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:00:37 2020

@author: djord
"""
import math
from typing import Callable, Any
from sri import preprocessing as prepro
import sri.Practice4.references as refs
import sri.Practice5.indexing as indexing

class QueryWFData(indexing.WFData):
    def __init__(self, wordid):
        super().__init__()
        self.wordid = wordid
        
    def __repr__(self):
        return "WordID: {0} ".format(self.wordid) + super().__repr__()

class Query:
    def __init__(self, originalquery: str):
        self.originalquery = originalquery
        self.words = {}
        self.maxfreq = -1
        self.norm = None
        self.prfextended = False
        
    def addword(self, word: str, wordid):
        hit= self.words.get(word)
        if (hit is None):
            hit = QueryWFData(wordid)
            self.words[word] = hit
        hit.increment()
        if (hit.freq > self.maxfreq):
            self.maxfreq = hit.freq
            
    def addprfword(self, wordid):
        self.prfextended = True
        
        founddata = None
        for _, qwfdata in self.words.items():
            if qwfdata.wordid == wordid:
                founddata = qwfdata
                break
        
        if founddata is None:
            founddata = QueryWFData(wordid)
            hsh = hash(wordid)
            self.words[hsh] = founddata
        founddata.increment()
        if (founddata.freq > self.maxfreq):
            self.maxfreq = founddata.freq
        
    def calcTFs(self):
        for _, qwfdata in self.words.items():
            qwfdata.calculateTF(self.maxfreq)
            
    def calcWs(self, idfgetmethod: Callable[[Any], float]):
        for _, qwfdata in self.words.items():
            qwfdata.calculateW(idfgetmethod(qwfdata.wordid))
            
    def calcWns(self):
        norm = self.calcNorm()
        for _, qwfdata in self.words.items():
            qwfdata.calculateWn(norm)  
        
    def calcNorm(self, recalc = False):
        if (self.norm is not None and not recalc):
            return self.norm
        
        sumOfSqrWs = 0
        for _, qwfdata in self.words.items():
            sumOfSqrWs += math.pow(qwfdata.w, 2)
            
        self.norm = math.sqrt(sumOfSqrWs)      
        return self.norm
    
    def isValid(self):
        if len(self.words) > 0:
            return True
        else:
            return False
    
    def __repr__(self):
        pairs = []
        pairs.append("Query: {0}".format(self.originalquery))
        for key,value in self.words.items():
            pairs.append("\tWord: {0} Data: {1}".format(key, value))
        pairs.append("\tMax freq: {0}".format(self.maxfreq))
        pairs.append("\tNorm: {0}".format(self.norm))
        return '\n'.join(pairs)

class QueryFactory:
    def __init__(self, s1prepro = prepro.Stage1Processor(), s2prepro = prepro.Stage2Processor("spanish")):
        self.s1prepro = s1prepro
        self.s2prepro = s2prepro
        
    def setIndexObjects(self, index: indexing.IndexingData, wordref: refs.WordRef):
        self.index = index
        self.wordref = wordref
        
    def processQueriesInFile(self, filepath: str) -> [Query]:
        queryres = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                sanitized = line.replace('\n', '').strip()
                if sanitized != '':
                    queryres.append(self.processQuery(sanitized))
        return queryres
        
    def processQueries(self, querylist: [str]) -> [Query]:
        queryres = []
        for query in querylist:
            queryres.append(self.processQuery(query))
        return queryres
    
    def processQuery(self, querystr: str) -> Query:
        tokens = self.s1prepro.processContent(querystr)
        stems = self.s2prepro.processWords(tokens)
        
        wordids = self.wordref.getWordIDs(stems)
        
        query = Query(querystr)
        
        for word,wordid in zip(stems, wordids):
            query.addword(word, wordid)
        query.calcTFs()
        query.calcWs(self.index.getwordidf)
        query.calcWns()
            
        return query
    
    def addPRFWords(self, query: Query, wordids: [int]) -> Query:
        for wordid in wordids:
            query.addprfword(wordid)
        
        query.calcTFs()
        query.calcWs(self.index.getwordidf)
        query.calcWns()
        return query