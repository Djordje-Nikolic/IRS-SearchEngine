# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 03:59:41 2020

@author: djord
"""
import os
import sri.Practice5.structures as structs
import helpers
import preprocessing as pp
from timeit import default_timer as timer

class StructureUtils:
    def __init__(self):
        self.preproctime = None
        self.calctime = None
        return
    
    def generateStructureWrapper(self, lang: str, collectionpath: str, middleoutput=False):
        structures = structs.StructureWrapper()
        self.s1preproc = pp.Stage1Processor()
        self.s2preproc = pp.Stage2Processor(lang)
          
        starttime = timer()     
        if middleoutput:
            middleoutpath = os.path.join(collectionpath, "middle_output")
            afters1path = os.path.join(middleoutpath, "stage1")
            afters2path = os.path.join(middleoutpath, "stage2")
            
            if not os.path.exists(afters1path):
                os.makedirs(afters1path)
            if not os.path.exists(afters2path):
                os.makedirs(afters2path)
            
            for tokens, filepath in self.s1preproc.processFolderGenerator(collectionpath):
                middleoutname = os.path.splitext(os.path.basename(filepath))[0] + ".txt"
                s1outpath = os.path.join(afters1path, middleoutname)
                s2outpath = os.path.join(afters2path, middleoutname)
                
                helpers.dumparraytofile(tokens, s1outpath)
                processedwords = self.s2preproc.processWords(tokens)
                
                helpers.dumparraytofile(processedwords, s2outpath)
                structures.addfile(processedwords, filepath)
        else:
            for tokens, filepath in self.s1preproc.processFolderGenerator(collectionpath):
                processedwords = self.s2preproc.processWords(tokens)
                structures.addfile(processedwords, filepath)               
        self.preproctime = timer() - starttime
                
        starttime = timer()
        structures.calculateFull()
        self.calctime = timer() - starttime
        
        return structures