# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 05:46:55 2020

@author: djord
"""
import sys
import os

syspaths = []
syspaths.append(os.path.abspath(".."))
syspaths.append(os.path.abspath(os.path.dirname(__file__)))
syspaths.append(os.path.abspath(".\Practice1"))
syspaths.append(os.path.abspath(".\Practice2"))
syspaths.append(os.path.abspath(".\Practice3"))
syspaths.append(os.path.abspath(".\Practice4"))
syspaths.append(os.path.abspath(".\Practice5"))
syspaths.append(os.path.abspath(".\Practice6"))
syspaths.append(os.path.abspath(".\Practice7"))

for path in syspaths:
    if (path not in sys.path):
        sys.path.append(path)

from structures_utils import StructureUtils
import sri.Practice6.config as config
import sri.Practice5.structures as structs
import Practice6.queryhandling as queryhandling
import Practice7.similarity as similarity

class SearchEngine:
    def __init__(self, configfilepath: str, genmiddleoutput = False, displayprocesstime = False):
        self.structpath, self.collectpath = config.parse(configfilepath)
        
        try:
            if (self.structpath is not None and os.path.exists(self.structpath)):
                self.structures = structs.StructureWrapper(folderpath = self.structpath)
            else:
                raise Exception("Index path is not correct")
                
#            try:
#                # if (self.collectpath is not None):
#                    # add files to index
#            except as err:
#                raise Exception("Couldn't add files to the loaded index: ", err) 
                
        except Exception as err:           
            if (self.collectpath is None or not os.path.exists(self.collectpath)):
                raise Exception("Couldn't load index and couldn't create an index from the files in the supplied collection: ", err)
            else:
                try:
                    structutils = StructureUtils()
                    self.structures = structutils.generateStructureWrapper("spanish", self.collectpath, middleoutput=genmiddleoutput)
                    
                    if displayprocesstime:
                        print("Preprocessing time: {0}s".format(structutils.preproctime))
                        print("Calculating time: {0}s".format(structutils.calctime))
                
                except Exception as err:
                    raise Exception("Couldn't create an index from the files in the supplied collection: ", err)
                
        self.queryfactory = queryhandling.QueryFactory()
        self.queryfactory.setIndexObjects(self.structures.index, self.structures.wordref)
        self.similaritygenerator = similarity.SimilarityGenerator(self.structures.index)
        
    def search(self, query: str, documentstoreturn = None, outputpath = None, fullfilepath = False):
        queryobj = self.queryfactory.processQuery(query)
        similarities = self.similaritygenerator.getSimilarities(queryobj)
        
        similarity.display(similarities, fullpath=fullfilepath, outfilepath=outputpath, maximumdocs=documentstoreturn)
        
    def searchFromFile(self, filepath: str, documentstoreturn = None, outputfolderpath = None, fullfilepath = False):
        queryobjs = self.queryfactory.processQueriesInFile(filepath)
        
        if (outputfolderpath is None):
            for queryobj in queryobjs:
                similarities = self.similaritygenerator.getSimilarities(queryobj)
                similarity.display(similarities, fullpath=fullfilepath, maximumdocs=documentstoreturn)
        else:
            counter = 1
            filename = "queryres{0}.txt"
            for queryobj in queryobjs:
                similarities = self.similaritygenerator.getSimilarities(queryobj)
                outputpath = os.path.join(outputfolderpath, filename.format(counter))
                similarity.display(similarities, fullpath=fullfilepath, outfilepath=outputpath, maximumdocs=documentstoreturn)
                counter += 1
            
    def save(self, folderpath: str = None):
        if folderpath is None:
            if self.structpath is not None:
                if not os.path.exists(self.structpath):
                    os.makedirs(self.structpath)
                self.structures.dump(self.structpath)
        else:
            self.structures.dump(folderpath)
      
#change this
#args = sys.argv
#configfilepath = args[1]
#queryfilepath = args[2]
#maxdocuments = int(args[3])
            
configfilepath = "C:\\Users\\djord\\source\\repos\\PyCharm Projects\\SRIProject\\sri\\config.txt"
queryfilepath = "C:\\Users\\djord\\source\\repos\\PyCharm Projects\\SRIProject\\sri\\queries.txt"
maxdocuments = 10

try:
    searchengine = SearchEngine(configfilepath, genmiddleoutput=False, displayprocesstime=True)
    
    queryfolder = os.path.dirname(queryfilepath)
    queryresfolder = "Query Results"
    queryrespath = os.path.join(queryfolder, queryresfolder)
    if not os.path.exists(queryrespath):
        os.makedirs(queryrespath)
    
    searchengine.searchFromFile(queryfilepath, documentstoreturn=maxdocuments, outputfolderpath=queryrespath)
    searchengine.save()
except Exception as err:
    print("Search engine exception: ", err)


