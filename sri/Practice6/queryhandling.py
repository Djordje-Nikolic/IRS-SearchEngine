# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:00:37 2020

@author: djord
"""
import math
from typing import Callable, Any
import sri.Practice1.normalizer_tokenizer as normtok
import sri.Practice2.stopper as stop
import sri.Practice3.stemmer as stem
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
        
    def addword(self, word: str, wordid):
        hit= self.words.get(word)
        if (hit is None):
            hit = QueryWFData(wordid)
            self.words[word] = hit
        hit.increment()
        if (hit.freq > self.maxfreq):
            self.maxfreq = hit.freq
        
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
    
    def __repr__(self):
        pairs = []
        pairs.append("Query: {0}".format(self.originalquery))
        for key,value in self.words.items():
            pairs.append("\tWord: {0} Data: {1}".format(key, value))
        pairs.append("\tMax freq: {0}".format(self.maxfreq))
        pairs.append("\tNorm: {0}".format(self.norm))
        return '\n'.join(pairs)

class QueryFactory:
    def __init__(self, normalizer = normtok.Normalizer(), tokenizer = normtok.Tokenizer(), stopper = stop.Stopper(), stemmer = stem.SpanishModStemmer()):
        self.normalizer = normalizer
        self.tokenizer = tokenizer
        self.stopper = stopper
        self.stemmer = stemmer
        
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
        normalized = self.normalizer.normalize(querystr)
        tokens = self.tokenizer.tokenize(normalized)
        tokenswithnostops = self.stopper.removestops(tokens)
        stems = list(map(self.stemmer.stem, tokenswithnostops))
        
        wordids = self.wordref.getWordIDs(stems)
        
        query = Query(querystr)
        
        for word,wordid in zip(stems, wordids):
            query.addword(word, wordid)
        query.calcTFs()
        query.calcWs(self.index.getwordidf)
        query.calcWns()
            
        return query