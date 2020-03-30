# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 01:06:44 2020

@author: djord
"""

import sys
import metadata
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

import helpers
from os.path import dirname
from os.path import join
from timeit import default_timer as timer
from Practice1.htmlfilter import HtmlFilter
from Practice1.normalizer_tokenizer import normalize_tokenizetofile
from Practice1.normalizer_tokenizer import normalize_tokenize
from Practice2.stopper import Stopper
from Practice3.stemmer import SpanishModStemmer

 # constants
rootpath = dirname(__file__)
corpusrelpath = "coleccionESuja2019//coleccionESuja2019"
outputfolder = "output"
metadatafolder = "metadata"
practice1output = "Practice1"
practice2output = "stopper"
practice3output = "stemmer"

 # path calculations
corpuspath = join(rootpath, corpusrelpath)
 
p1outpath = join(rootpath, outputfolder, practice1output)
p2outpath = join(rootpath, outputfolder, practice2output)
p3outpath = join(rootpath, outputfolder, practice3output)
metaoutpath = join(rootpath, metadatafolder)
if not os.path.exists(p1outpath):
    os.makedirs(p1outpath)
if not os.path.exists(p2outpath):
    os.makedirs(p2outpath) 
if not os.path.exists(p3outpath):
    os.makedirs(p3outpath) 
if not os.path.exists(metaoutpath):
    os.makedirs(metaoutpath)

    
p1metadata = metadata.Metadata1()

p2beforemdata = metadata.Metadata2("Metadata2 (Practice2 - before stop words removal)")
p2aftermdata = metadata.Metadata2("Metadata2 (Practice2 - after stop words removal)")   
  
p3beforemdata = p2aftermdata
p3aftermdata = metadata.Metadata2("Metadata2 (Practice3 - after stemming)")   

p1totaltime = 0.0
p2totaltime = 0.0
p3totaltime = 0.0

starttime = timer()

# Practice 1 init

# Practice 2 Init
stopper = Stopper(metadataBefore = p2beforemdata, metadataAfter = p2aftermdata)
p2totaltime += timer() - starttime

# Practice 3 init
stemmer = SpanishModStemmer()

for filename in os.listdir(corpuspath):
    filepath = join(corpuspath, filename)
    if not os.path.isfile(filepath):
        continue
    
    ### <Practice1>
    p1starttime = timer()
    
    outputfilepath = join(p1outpath, os.path.splitext(filename)[0] + ".txt")
    
    htmlfilter = HtmlFilter(filepath)
    htmlfilter.filterContent()
    filteredtext = htmlfilter.getContent()
    
    tokens = normalize_tokenize(filteredtext, metadata=p1metadata)
    helpers.dumparraytofile(tokens, outputfilepath)
    
    p1totaltime += timer() - p1starttime
    ### </Practice1>
    
    ### <Practice2>
    p2starttime = timer()
    
    outputfilepath = join(p2outpath, os.path.splitext(filename)[0] + ".txt")
    
    tokenswithnostops = stopper.removestops(tokens)
    helpers.dumparraytofile(tokenswithnostops, outputfilepath)
    
    p2totaltime += timer() - p2starttime
    ### </Practice2>
    
    ### <Practice3>
    p3starttime = timer()
    
    outputfilepath = join(p3outpath, os.path.splitext(filename)[0] + ".txt")
    
    stems = []
    for token in tokenswithnostops:
        stems.append(stemmer.stem(token))
    p3aftermdata.countFile(stems)
    helpers.dumparraytofile(stems, outputfilepath)
    
    p3totaltime += timer() - p3starttime
    ### </Practice3>
      
endtime = timer()
print("Practice 1 processing time taken: ", p1totaltime)
print("Practice 2 processing time taken: ", p2totaltime)
print("Practice 3 processing time taken: ", p3totaltime)
print("Total time taken: ", endtime - starttime)

p1metadata.setTimeTaken(p1totaltime)
p1metadata.dumpInfo(join(metaoutpath, "metadataP1.txt"))

p2beforemdata.setTimeTaken(p2totaltime)
p2beforemdata.dumpInfo(join(metaoutpath, "metadataP2Before.txt"))
p2aftermdata.setTimeTaken(p2totaltime)
p2aftermdata.dumpInfo(join(metaoutpath, "metadataP2After.txt"))

p3beforemdata.setTitle("Metadata2 (Practice3 - before stemming)")
p3beforemdata.setTimeTaken(p3totaltime)
p3beforemdata.dumpInfo(join(metaoutpath, "metadataP3Before.txt"))
p3aftermdata.setTimeTaken(p3totaltime)
p3aftermdata.dumpInfo(join(metaoutpath, "metadataP3After.txt"))