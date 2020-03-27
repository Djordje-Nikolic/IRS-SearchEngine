# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 01:06:44 2020

@author: djord
"""

import sys
import metadata
import os

#sys.path.insert(0, os.path.dirname(__file__))

from os.path import dirname
from os.path import join
from timeit import default_timer as timer
from Practice1.htmlfilter import HtmlFilter
from Practice1.normalizer_tokenizer import readtokens_fromfile
from Practice2.stopper import Stopper
from Practice3.stemmer import SpanishModStemmer
import Practice4.indexing as indexing
import Practice4.references as refs

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
p3outpath = join(rootpath, outputfolder, practice3output)

metaoutpath = join(rootpath, metadatafolder)
if not os.path.exists(metaoutpath):
    os.makedirs(metaoutpath)

p4totaltime = 0.0

starttime = timer()

# Practice 4 init
wordrefs = refs.WordRef()
filerefs = refs.FileRef()
indexingdata = indexing.IndexingData()

p4mdata = metadata.Metadata3(structuretosize=indexingdata)

for filename in os.listdir(corpuspath):
    filepath = join(corpuspath, filename)
    if not os.path.isfile(filepath):
        continue
    
    ### <Practice4>
    # calculate path for the P3 stemmed output
    p4starttime = timer()
    
    p3filepath = join(p3outpath, os.path.splitext(filename)[0] + ".txt")
    tokens = readtokens_fromfile(p3filepath)
    
    # we save the path to the original html file
    fileid = filerefs.addFile(filepath)
    
    for word in tokens:
        wordid = wordrefs.addWord(word)
        indexingdata.countWord(wordid, fileid)
        
    p4totaltime += timer() - p4starttime
    ### </Practice4>
    
     
endtime = timer()
print("Total time taken: ", endtime - starttime)

p4mdata.setTimeTaken(p4totaltime)
p4mdata.dumpInfo(join(metaoutpath, "metadataP4.txt"))

indexingdata.dumpInfo(join(metaoutpath, "indexingstruct.txt"))