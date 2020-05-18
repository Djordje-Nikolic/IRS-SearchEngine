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
    def __init__(self, configfilepath: str, genmiddleoutput: bool = False, displayprocesstime: bool = False):
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
                    self.save()
                    
                    if displayprocesstime:
                        print("Preprocessing time: {0}s".format(structutils.preproctime))
                        print("Calculating time: {0}s".format(structutils.calctime))
                
                except Exception as err:
                    raise Exception("Couldn't create an index from the files in the supplied collection: ", err)
                
        self.queryfactory = queryhandling.QueryFactory()
        self.queryfactory.setIndexObjects(self.structures.index, self.structures.wordref)
        self.similaritygenerator = similarity.SimilarityGenerator(self.structures.index, normalize=False, prfwordcount = 5, queryfactory=self.queryfactory)
        
    def search(self, query: str, documentstoreturn: int = None, outputpath: str = None, fullfilepath: str = False, returnobjects: bool = False, prf: bool = False):
        queryobj = self.queryfactory.processQuery(query)
        similarities = self.similaritygenerator.getSimilarities(queryobj, prf=prf)
        
        if returnobjects:
            return similarities
        
        similarity.display(similarities, fullpath=fullfilepath, outfilepath=outputpath, maximumdocs=documentstoreturn)
        
    def searchFromFile(self, filepath: str, documentstoreturn: int = None, outputfolderpath: str = None, fullfilepath: bool = False, prf: bool = False):
        queryobjs = self.queryfactory.processQueriesInFile(filepath)
        
        if (outputfolderpath is None):
            for queryobj in queryobjs:
                similarities = self.similaritygenerator.getSimilarities(queryobj, prf=prf)
                similarity.display(similarities, fullpath=fullfilepath, maximumdocs=documentstoreturn)
        else:
            counter = 1
            filename = "queryres{0}.txt"
            for queryobj in queryobjs:
                similarities = self.similaritygenerator.getSimilarities(queryobj, prf=prf)
                outputpath = os.path.join(outputfolderpath, filename.format(counter))
                similarity.display(similarities, fullpath=fullfilepath, outfilepath=outputpath, maximumdocs=documentstoreturn)
                counter += 1
        
    def getFileContent(self, fileid):
        try:
            filepath = self.structures.fileref.getFilepath(fileid)
            
            content = ""
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            return content
        except Exception as err:
            # should log           
            print("Error getting content for fileid '{0}':".format(fileid), err)
            return ""
    
    def save(self, folderpath: str = None):
        if folderpath is None:
            if self.structpath is not None:
                if not os.path.exists(self.structpath):
                    os.makedirs(self.structpath)
                self.structures.dump(self.structpath)
        else:
            self.structures.dump(folderpath)
      
        
if __name__ == '__main__':
    # Execute as script
    
    if (len(sys.argv) != 4):
        print("If executed as a script, this module needs 3 input arguments.")
        print("\t - full path to the config file")
        print("\t - full path to the file containing queries to be searched")
        print("\t - number of documents to be returned as result")
        sys.exit()
    
    #change this
    args = sys.argv
    configfilepath = args[1]
    queryfilepath = args[2]
    maxdocuments = int(args[3])
    
    try:
        searchengine = SearchEngine(configfilepath, genmiddleoutput=True, displayprocesstime=True)
        
        queryfolder = os.path.dirname(queryfilepath)
        queryresfolder = "Query Results"
        queryrespath = os.path.join(queryfolder, queryresfolder)
        if not os.path.exists(queryrespath):
            os.makedirs(queryrespath)
        
        searchengine.searchFromFile(queryfilepath, documentstoreturn=maxdocuments, outputfolderpath=queryrespath)
        
        searchengine.save()
    except Exception as err:
        print("Search engine exception: ", err)