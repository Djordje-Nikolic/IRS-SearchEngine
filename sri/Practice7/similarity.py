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
        
class Similarities:
    def __init__(self, originalquery: str):
        self.list = []
        self.timetaken = None
        self.originalquery = originalquery
        
    def addsimilarity(self, fileid, similarity: float, fileref: refs.FileRef = None):
        sim = Similarity(fileid, similarity)    
        if (fileref is not None):
            sim.setfilepath(fileref.getFilepath(sim.fileid))  
        self.list.append(sim)
        
    def setTimeTaken(self, timetaken):
        self.timetaken = timetaken
        
    def sort(self):
        self.list = sorted(self.list, reverse=True, key=lambda sim: sim.value)
    
    def dumpInfo(self, filepath: str = None, topcount = None):
        display(self, orgquery = True, outfilepath = filepath, maximumdocs = topcount)
    
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
    def __init__(self, index: indexing.IndexingData):
        self.index = index
        
    def getSimilarities(self, query: queryhandling.Query) -> Similarities:
        similarities = Similarities(query.originalquery)
        
        starttime = timer()
        for fileid, norm in self.index.norms.items():
            dividend = self.calcSimDividend(query, fileid)
            divisor = self.calcSimDivisor(query, norm)
            similarity = dividend / divisor
            
            # ignore file if similarity is not greater than 0
            if similarity > 0:
                similarities.addsimilarity(fileid, similarity, fileref = self.index.fileref)
        endtime = timer()
        similarities.setTimeTaken(endtime - starttime)        
        
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