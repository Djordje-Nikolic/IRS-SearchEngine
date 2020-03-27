# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 01:16:50 2020

@author: djord
"""
import sys
import os
from pickle import dump,load

import sri.Practice5.indexing as indexing
import sri.Practice4.references as references

from typing import Tuple


wordreffilename = "wordref.sribk"
filereffilename = "fileref.sribk"
indexfilename = "index.sribk"

def dumpStructures(wordref: references.WordRef, fileref: references.FileRef, index: indexing.IndexingData, folderpath: str):
    with open(os.path.join(folderpath, wordreffilename), "wb") as f:
        dump(wordref, f)
    with open(os.path.join(folderpath, filereffilename), "wb") as f:
        dump(fileref, f)
    with open(os.path.join(folderpath, indexfilename), "wb") as f:
        dump(index, f)
        
def loadStructures(folderpath: str) -> Tuple[references.WordRef, references.FileRef, indexing.IndexingData]:
    with open(os.path.join(folderpath, wordreffilename), "rb") as f:
        wordref = load(f)
    with open(os.path.join(folderpath, filereffilename), "rb") as f:
        fileref = load(f)
    with open(os.path.join(folderpath, indexfilename), "rb") as f:
        index = load(f)
    index.setFileRef(fileref)
    return wordref, fileref, index