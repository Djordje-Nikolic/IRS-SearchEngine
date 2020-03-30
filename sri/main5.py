# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 01:06:44 2020

@author: djord
"""
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

from os.path import dirname
from os.path import join
from timeit import default_timer as timer

from Practice1.normalizer_tokenizer import readtokens_fromfile
import Practice4.references as refs
import Practice5.indexing as indexing
import Practice5.structures_serialization as structserial

 # constants
rootpath = dirname(__file__)
corpusrelpath = "coleccionESuja2019//coleccionESuja2019"
outputfolder = "output"
metadatafolder = "metadata"
practice1output = "Practice1"
practice2output = "stopper"
practice3output = "stemmer"
practice5output = "structures"

 # path calculations
corpuspath = join(rootpath, corpusrelpath)
p3outpath = join(rootpath, outputfolder, practice3output)
p5outpath = join(rootpath, outputfolder, practice5output)

metaoutpath = join(rootpath, metadatafolder)
if not os.path.exists(metaoutpath):
    os.makedirs(metaoutpath)
if not os.path.exists(p5outpath):
    os.makedirs(p5outpath)

# Practice 4 structures init, we create these again because we are using a different version of the indexing structures from the P4
wordrefs = refs.WordRef()
filerefs = refs.FileRef()
indexdata = indexing.IndexingData()
indexdata.setFileRef(filerefs)

for filename in os.listdir(corpuspath):
    filepath = join(corpuspath, filename)
    if not os.path.isfile(filepath):
        continue
    
    p3filepath = join(p3outpath, os.path.splitext(filename)[0] + ".txt")
    tokens = readtokens_fromfile(p3filepath)
    
    # we save the path to the original html file
    fileid = filerefs.addFile(filepath)
    
    for word in tokens:
        wordid = wordrefs.addWord(word)
        indexdata.countWord(wordid, fileid)

p5mdata = metadata.Metadata3(structuretosize=indexdata)

# Weight calculations
starttime = timer()
### <Practice5>
indexdata.calculateFull()
### </Practice5>
endtime = timer()

p5mdata.setTimeTaken(endtime - starttime)
p5mdata.dumpInfo(join(metaoutpath, "metadataP5.txt"))

indexdata.dumpInfo(join(metaoutpath, "indexdata.txt")) 
structserial.dumpStructures(wordrefs, filerefs, indexdata, p5outpath)

print("Total time taken: ", endtime - starttime)