# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 05:10:50 2020

@author: djord
"""
from timeit import default_timer as timer
from os.path import basename
import sri.Practice4.references as refs
import sri.Practice5.indexing as indexing
import sri.Practice6.queryhandling as queryhandling
        
class Similarity:
    def __init__(self, fileid: str, simvalue: float, filepath: str = None):
        self.fileid = fileid
        self.value = simvalue
        self.filepath = None
        
    def setfilepath(self, filepath: str):
        self.filepath = filepath
        
    def getfilename(self):
        return basename(self.filepath)
    
    def getdesc(self, fullpath = False):
        if (self.filepath is None):
            return self.fileid
        else:
            if fullpath:
                return self.filepath
            else:
                return self.getfilename()
                
    def serialize(self, fulldesc: bool = False):
        return {
            'fileid' : str(self.fileid),
            'value' : self.value,
            'filedesc' : self.getdesc(fullpath = fulldesc),
        }
        
class Similarities:
    def __init__(self, originalquery: str):
        self.list = []
        self.timetaken = None
        self.originalquery = originalquery
        self.isSorted = False
        
    def addsimilarity(self, fileid, similarity: float, fileref: refs.FileRef = None):
        sim = Similarity(fileid, similarity)    
        if (fileref is not None):
            sim.setfilepath(fileref.getFilepath(sim.fileid))  
        self.list.append(sim)       
        self.isSorted = False
        
    def setTimeTaken(self, timetaken):
        self.timetaken = timetaken
        
    def sort(self):
        if not self.isSorted:
            self.list = sorted(self.list, reverse=True, key=lambda sim: sim.value)
            self.isSorted = True
    
    def dumpInfo(self, filepath: str = None, topcount = None):
        display(self, orgquery = True, outfilepath = filepath, maximumdocs = topcount)
        
    def serialize(self, fullfilepath: bool = False, offset: int = 0, count: int = None):
        if count is None:
            return {
                'totalcount' : len(self.list),
                'timetaken' : self.timetaken,
                'originalquery' : self.originalquery,
                'similarities' : [s.serialize(fulldesc = fullfilepath) for s in self.list[offset:]]
            }
        else:
            return {
                'totalcount' : len(self.list),
                'timetaken' : self.timetaken,
                'originalquery' : self.originalquery,
                'similarities' : [s.serialize(fulldesc = fullfilepath) for s in self.list[offset:offset + count]]
            }
    
def display(sims: Similarities, fullpath = False, outfilepath = None, maximumdocs = None, sort = True, orgquery = True):
    lines = []
    if (orgquery):
        lines.append("\"{0}\"".format(sims.originalquery))
        

    if (sort):
        sims.sort()
        
    simlist = sims.list
        
    if (maximumdocs is None):
        maximumdocs = len(simlist)
    else:
        maximumdocs = min(maximumdocs, len(simlist))
        
    counter = 0
    while counter < maximumdocs:
        sim = simlist[counter]
        lines.append("\t{0:2d}. {1:.5f}\t{2}".format(counter + 1, sim.value, sim.getdesc(fullpath = fullpath)))
        counter += 1
        
    lines.append("Time taken: {0:.5f}s Number of similarities: {1}".format(sims.timetaken,len(simlist)))
    output = '\n'.join(lines)
    
    if (outfilepath is None):
        print(output)
    else:
        with open(outfilepath, "w") as f:
            print(output, file = f)
        
class SimilarityGenerator():
    def __init__(self, index: indexing.IndexingData, normalize: bool = False, prfwordcount: int = None, queryfactory: queryhandling.QueryFactory = None):
        self.index = index
        self.normalize = normalize  
        self.queryfactory = queryfactory
        
        if prfwordcount is not None:
            self.prfstruct = self.index.getMostCommonWords(count = prfwordcount)
        else:
            self.prfstruct = None
        
    def getSimilarities(self, query: queryhandling.Query, prf: bool = False, prffilecount: int = 5) -> Similarities:        
        similarities = None
        
        starttime = timer()
        
        if prf and self.queryfactory:
            firstsimilarities = self.genSimilarities(query)
            firstsimilarities.sort()
            
            prfwordids = []
            for similarity in firstsimilarities.list[:prffilecount]:
                wordids = self.getPRFWordIDs(similarity.fileid)
                prfwordids.extend(wordids)
                
            newquery = self.queryfactory.addPRFWords(query, prfwordids)
            similarities = self.genSimilarities(newquery)               
        else:
            similarities = self.genSimilarities(query)
        
        endtime = timer()
        similarities.setTimeTaken(endtime - starttime)        
        
        return similarities
    
    def genSimilarities(self, query):
        similarities = Similarities(query.originalquery)
        
        if self.normalize:
            for fileid, norm in self.index.norms.items():
                
                if query.isValid():
                    dividend = self.calcSimDividend(query, fileid)
                    divisor = self.calcSimDivisor(query, norm)           
                    similarity = dividend / divisor
                else:
                    similarity = 0
                
                # ignore file if similarity is not greater than 0
                if similarity > 0:
                    similarities.addsimilarity(fileid, similarity, fileref = self.index.fileref)
        else:
            for fileid, norm in self.index.norms.items():
                
                similarity = self.calcSimDividend(query, fileid)
             
                # ignore file if similarity is not greater than 0
                if similarity > 0:
                    similarities.addsimilarity(fileid, similarity, fileref = self.index.fileref)
            
        return similarities    
            
    def calcSimDividend(self, query: queryhandling.Query, fileid):
        sumOfWProds = 0
        for word, qwfdata in query.words.items():
            querywn = qwfdata.wn
            indexworddata = self.index.getwordinfo(qwfdata.wordid)
            if (indexworddata is None):
                continue            
            indexwfdata = indexworddata.getwfdata(fileid)
            if (indexwfdata is None):
                continue
            localprod = indexwfdata.wn * querywn
            sumOfWProds += localprod
        return sumOfWProds        
        
    def calcSimDivisor(self, query: queryhandling.Query, filenorm):
        return query.calcNorm() * filenorm

    def getPRFWordIDs(self, fileid):
        words = []
        if self.prfstruct and self.queryfactory:
            filedata = self.prfstruct.get(fileid)
            for wordid, _ in filedata:
                words.append(wordid)
                
        return words
        
    