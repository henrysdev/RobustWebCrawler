# Henry Warren 2018
# hwarren@smu.edu

class Indexer():
    def __init__(self, master):
        self.master = master
        self.termFreqMatrix = {}
        self.docNum = 0

    def indexDoc(self, words, url):
        print("indexing: {}\nword count: {}".format(url, len(words)))
        print("words: {}".format(words))
        if len(words) == 0:
            print("no words to index")
            return
        docId = "doc"+str(self.docNum)
        self.termFreqMatrix[docId] = {}
        for word in words:
            if word not in self.termFreqMatrix[docId]:
                self.termFreqMatrix[docId][word] = 0
            if word in self.termFreqMatrix[docId]:
                self.termFreqMatrix[docId][word] += 1
        self.docNum += 1

    def getNMostFrequent(self, N, mode="tf"):
        if mode not in ["tf", "df"]:
            print("invalid mode passed to getNMostFrequent. Returning")
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