# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 01:06:44 2020

@author: djord
"""
import os
from os.path import dirname
from os.path import join

from timeit import default_timer as timer
import Practice5.structures_serialization as structserial
import Practice6.queryhandling as queryhandling
import Practice7.similarity as similarity

 # constants
rootpath = dirname(__file__)
corpusrelpath = "coleccionESuja2019//coleccionESuja2019"
outputfolder = "output"
metadatafolder = "metadata"
practice1output = "Practice1"
practice2output = "stopper"
practice3output = "stemmer"
practice5output = "structures"
practice6output = "query_results"
queryfilename = "queries.txt"

 # path calculations
corpuspath = join(rootpath, corpusrelpath)
p3outpath = join(rootpath, outputfolder, practice3output)
p5outpath = join(rootpath, outputfolder, practice5output)
p6outpath = join(rootpath, outputfolder, practice6output)
queryfilepath = join(rootpath, queryfilename)

metaoutpath = join(rootpath, metadatafolder)
if not os.path.exists(metaoutpath):
    os.makedirs(metaoutpath)
if not os.path.exists(p6outpath):
    os.makedirs(p6outpath)

# Practice 5 structures load 
wordrefs, filerefs, index = structserial.loadStructures(p5outpath)

# Practice 6 structures init
queryfactory = queryhandling.QueryFactory()
queryfactory.setIndexObjects(index, wordrefs)
similaritygenerator = similarity.SimilarityGenerator(index)

### <Practice6>
counter = 1
queries = queryfactory.processQueriesInFile(queryfilepath)
for query in queries:
    sim = similaritygenerator.getSimilarities(query)
    
#    sim.dumpInfo(join(p6outpath, "query{0}.txt".format(counter)))
    sim.dumpInfo(topcount = 10)
    counter += 1
### </Practice6>