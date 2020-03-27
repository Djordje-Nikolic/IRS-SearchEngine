# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 23:57:18 2020

@author: djord
"""
import os
import sri.Practice4.references as refs
import sri.Practice5.indexing as indexing
import sri.Practice5.structures_serialization as serialization

class StructureWrapper:
    def __init__(self, folderpath: str = None):
        if folderpath is not None:
            self.load(folderpath)
        else:
            self.wordref = refs.WordRef()
            self.fileref = refs.FileRef()
            self.index = indexing.IndexingData()
            self.index.setFileRef(self.fileref)
        
    def addfile(self, preprocessedwords: [str], filepath: str):
        fileid = self.fileref.addFile(filepath)
        
        for word in preprocessedwords:
            wordid = self.wordref.addWord(word)
            self.index.countWord(wordid, fileid)
            
    def calculateFull(self):
        self.index.calculateFull()
    
    def dump(self, folderpath: str):
        if not os.path.isfile(folderpath):
            serialization.dumpStructures(self.wordref, self.fileref, self.index, folderpath)
            
    def load(self, folderpath: str):
        if not os.path.isfile(folderpath):
            self.wordref, self.fileref, self.index = serialization.loadStructures(folderpath)