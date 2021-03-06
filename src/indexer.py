# Henry Warren 2018
# hwarren@smu.edu

import csv
import sys

class Indexer():
    def __init__(self):
        self.tfMatrix = {}
        self.docUrls = {}
        self.docNum = 0
        self.allWords = []


    # add entries to term frequency matrix via nested 
    # dictionaries to simulate a 2-D array
    def indexDoc(self, words, url, title):
        if len(words) == 0:
            return
        docId = title
        self.docUrls[docId] = url
        self.tfMatrix[docId] = {}
        for word in words:
            if word not in self.tfMatrix[docId]:
                self.tfMatrix[docId][word] = 0
            if word in self.tfMatrix[docId]:
                self.tfMatrix[docId][word] += 1
        self.docNum += 1


    # get comprehensive list of words and fill in 
    # empty cells with zeros
    def buildMatrix(self):
        # get a list of all unique words
        for doc in self.tfMatrix:
            for word in self.tfMatrix[doc]:
                if word not in self.allWords:
                    self.allWords.append(word)
        # fill in zeros where words do not exist
        for doc in self.tfMatrix:
            for word in self.allWords:
                if word not in self.tfMatrix[doc]:
                    self.tfMatrix[doc][word] = 0


    # output matrix to a .csv file
    def matrixToCsv(self, out):
        self.buildMatrix()
        fields = ['Document', 'Url'] + self.allWords
        with open(out, 'w') as f:
            w = csv.DictWriter(f, fields)
            w.writeheader()
            for key,val in sorted(self.tfMatrix.items()):
                row = {'Document': key, 'Url': self.docUrls[key]}
                row.update(val)
                w.writerow(row)


    # find N most frequent words (by either term-frequency
    # or document-frequency) in the saved matrix and return
    # them as tuples
    def getNMostFrequent(self, N):
        self.matrixToCsv('out/term-frequency.csv')
        allWords = {}
        allWords["tf"] = {}
        allWords["df"] = {}
        for doc in self.tfMatrix:
            for word in self.tfMatrix[doc]:
                if word in allWords["tf"]:
                    allWords["tf"][word] += self.tfMatrix[doc][word]
                if word in allWords["df"]:
                    allWords["df"][word] += 1
                if word not in allWords["tf"]:
                    allWords["tf"][word] = self.tfMatrix[doc][word]
                if word not in allWords["df"]:
                    allWords["df"][word] = 1

        rankedWords = []
        for word in allWords["tf"]:
            rankedWords.append((word,allWords["tf"][word],allWords["df"][word]))

        rankedWords.sort(key=lambda x: x[1], reverse=True)
        if N > len(rankedWords):
            return rankedWords
        else:
            return rankedWords[:N]