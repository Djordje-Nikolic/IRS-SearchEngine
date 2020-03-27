# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 02:18:07 2020

@author: djord
"""
import helpers

class Metadata1:
    def __init__(self, title = "Metadata1 (Practice1)"):
        self.title = title
        self.filecount = 0
        self.totaltokencount = 0
        self.timetaken = 0.0
        
    def countFile(self, tokencount: int):
        self.filecount += 1
        self.totaltokencount += tokencount
        
    def dumpInfo(self, filepath = None):
        mainstring = "{0} stats: ".format(self.title)
        filesstring = "\tFiles processed: {0}".format(self.filecount)
        totaltokens = "\tTotal collection tokens: {0}".format(self.totaltokencount)
        averagetokens = "\tAverage tokens per file: {0}".format(self.totaltokencount / self.filecount)
        timestring = "\tTime taken: {0}".format(self.timetaken)
        
        if filepath is not None:
            with open(filepath, "w") as output:
                print(mainstring,file=output)
                print(filesstring,file=output)
                print(totaltokens,file=output)
                print(averagetokens,file=output)
                print(timestring,file=output)
        
        print(mainstring)
        print(filesstring)
        print(totaltokens)
        print(averagetokens)
        print(timestring)
        
    def setTimeTaken(self, time):
        self.timetaken = time
        
class Metadata2(Metadata1):
    def __init__(self, title: str):
        super().__init__(self)
        self.minimumwordcount = 20000000
        self.maximumwordcount = -1
        self.wordfrequency = {}
        self.title = title
        
    def setTitle(self, title: str):
        self.title = title
        
    def countFile(self, words: [str]):
        wordcount = len(words)
        super().countFile(wordcount)
        
        if (wordcount < self.minimumwordcount):
            self.minimumwordcount = wordcount
            
        if (wordcount > self.maximumwordcount):
            self.maximumwordcount = wordcount
            
        self.processWordsForFrequency(words)
        
    def processWordsForFrequency(self, words: [str]):
        for word in words:
            if (self.wordfrequency.get(word) is None):
                self.wordfrequency[word] = 1
            else:
                self.wordfrequency[word] += 1
                
    def dumpInfo(self, filepath = None, topcount = 5):
        mainstring = "{0} stats: ".format(self.title)
        filesstring = "\tFiles processed: {0}".format(self.filecount)
        totaltokens = "\tTotal word count: {0}".format(self.totaltokencount)
        averagetokens = "\tAverage words per file: {0}".format(self.totaltokencount / self.filecount)
        mintokens = "\tMinimum words in a file: {0}".format(self.minimumwordcount)
        maxtokens = "\tMaximum words in a file: {0}".format(self.maximumwordcount)
        frequencystat = self.generateTopNString(topcount)
        timestring = "\tTime taken: {0}".format(self.timetaken)
        
        if filepath is not None:
            with open(filepath, "w") as output:
                print(mainstring,file=output)
                print(filesstring,file=output)
                print(totaltokens,file=output)
                print(averagetokens,file=output)
                print(mintokens,file=output)
                print(maxtokens,file=output)
                print(frequencystat,file=output)
                print(timestring,file=output)
        
        print(mainstring)
        print(filesstring)
        print(totaltokens)
        print(averagetokens)
        print(mintokens)
        print(maxtokens)
        print(frequencystat)
        print(timestring)
        
    def generateTopNString(self, count = 5):
        sortedstats = sorted(self.wordfrequency.items(), key=lambda x: x[1], reverse=True)
        top = sortedstats[0:count]
        genstrings = []
        genstrings.append("\tTop {0} words by appearance:".format(count))
        counter = 1
        for stat in top:
            genstrings.append("{0}. Word: {1} Count: {2}".format(counter, stat[0], stat[1]))
            counter += 1
        return "\n\t\t".join(genstrings)
        
class Metadata3:
    def __init__(self, title = "Metadata3 (Practice 4)", structuretosize = None):
        self.title = title
        self.timetaken = 0.0
        self.structuretosize = structuretosize
        
    def dumpInfo(self, filepath: str):
        with open(filepath, "w") as f:
            print("Time taken: {0}".format(self.timetaken), file=f)
            print("Structure info: ", file=f)
            print(self.generateStructureSizeInfo(), file=f)
            print(helpers.generateMachineInfo(), file=f)
            
    def generateStructureSizeInfo(self):
        if (self.structuretosize is not None):
            return "Type: {0} Size: {1} b".format(type(self.structuretosize), helpers.getsize(self.structuretosize))
        else:
            return None
        
    def setTimeTaken(self, time):
        self.timetaken = time