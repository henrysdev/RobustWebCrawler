# Henry Warren 2018
# hwarren@smu.edu

class Indexer():
    def __init__(self):
        self.termFreqMatrix = {}
        self.docNum = 0


    # add entries to term frequency matrix via nested dictionaries
    def indexDoc(self, words, url):
        if len(words) == 0:
            return
        docId = "doc"+str(self.docNum)
        self.termFreqMatrix[docId] = {}
        for word in words:
            if word not in self.termFreqMatrix[docId]:
                self.termFreqMatrix[docId][word] = 0
            if word in self.termFreqMatrix[docId]:
                self.termFreqMatrix[docId][word] += 1
        self.docNum += 1


    # find N most frequent words (by either term-frequency
    # or document-frequency) in the saved matrix and return
    # them as tuples
    def getNMostFrequent(self, N, mode="tf"):
        if mode not in ["tf", "df"]:
            return
        allWords = {}
        for doc in self.termFreqMatrix:
            for word in self.termFreqMatrix[doc]:
                if word in allWords:
                    if mode == "tf":
                        allWords[word] += self.termFreqMatrix[doc][word]
                    if mode == "df":
                        allWords[word] += 1
                else:
                    if mode == "tf":
                        allWords[word] = self.termFreqMatrix[doc][word]
                    if mode == "df":
                        allWords[word] = 1

        rankedWords = []
        for word in allWords:
            rankedWords.append((word,allWords[word]))

        rankedWords.sort(key=lambda x: x[1], reverse=True)
        if N > len(rankedWords):
            return rankedWords
        else:
            return rankedWords[:N]