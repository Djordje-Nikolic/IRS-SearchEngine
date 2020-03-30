# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 02:47:09 2020

@author: djord
"""
import os
import sri.Practice1.htmlfilter as htmlfilter
import sri.Practice1.normalizer_tokenizer as normtok
import sri.Practice2.stopper as stop
import sri.Practice3.stemmer as stem

class Stage1Processor:
    def __init__(self, filt = htmlfilter.HtmlFilter(), normalizer = normtok.Normalizer(), tokenizer = normtok.Tokenizer()):
        self.filter = filt
        self.normalizer = normalizer
        self.tokenizer = tokenizer
        
    def processContent(self, text: str):
        normalized = self.normalizer.normalize(text)
        return self.tokenizer.tokenize(normalized)
        
    def processFile(self, filepath: str):
        if os.path.isfile(filepath):
            self.filter.setFilepath(filepath)
            self.filter.filterContent()
            content = self.filter.getContent()
        
            return self.processContent(content)
        else:
            raise Exception
            
    def processFolderGenerator(self, folderpath: str):
        if not os.path.isfile(folderpath):
            for filename in os.listdir(folderpath):
                filepath = os.path.join(folderpath, filename)
                if os.path.isfile(filepath):
                    yield self.processFile(filepath), filepath
    
class Stage2Processor:
    def __init__(self, lang: str):
        if (lang == "spanish"):
            self.stopper = stop.Stopper()
            self.stemmer = stem.SpanishModStemmer()
        else:
            raise Exception
            
    def processWords(self, words: [str]):
        wordswithnostops = self.stopper.removestops(words)
        
        stems = []
        for word in wordswithnostops:
            stems.append(self.stemmer.stem(word))
        
        return stems