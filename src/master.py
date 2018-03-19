# Henry Warren 2018
# hwarren@smu.edu

from bs4 import BeautifulSoup
from time import sleep
import sys

from spider import Spider
from parser import Parser
from urlfilter import UrlFilter
from pagearchive import PageArchive
from indexer import Indexer
from urlfrontier import UrlFrontier


# managing object for controlling data flow in the crawler 
class MasterNode():
    def __init__(self, seedSet, stopWords):
        self.seedSet = seedSet
        self.stopWords = stopWords
        self.urlFront = UrlFrontier(seedSet)
        self.pageArchive = PageArchive()
        self.urlFilter = UrlFilter(self)
        self.indexer = Indexer()
        self.parser = Parser(self, 
                             self.urlFilter, 
                             self.pageArchive, 
                             self.indexer, 
                             self.stopWords
                             )
        self.spider = Spider(self, self.parser)
        self.crawlDelay = 1
        self.crawlRules = []
        self.testDataLinks = []
        self.duplicateLinks = []
        self.brokenLinks = []
        self.imageFiles = []
        self.outgoingLinks = []


    # set crawling rules found in robots.txt
    def setCrawlRules(self, rules):
        for r in rules:
            self.crawlRules.append((r[0],r[1]))
        for pair in self.crawlRules:
            key, val = pair
            if key == "Disallow":
                print("{}:{}".format(key,val))
                self.urlFilter.addRestrictedPath(val)
            if key == "User-agent":
                print("{}:{}".format(key,val))
                self.spider.setUserAgent(val)
            if key == "Crawl-delay":
                print("{}:{}".format(key,val))
                self.master.crawlDelay = val


    # try to find robots.txt
    def findRobotRules(self):
        for seedUrl in self.seedSet:
            robotsUrl = "{}{}".format(seedUrl, 
                                       "robots.txt")
            html = self.spider.crawl(robotsUrl, 
                                     rtnHtml=True)
        if len(self.crawlRules) == 0:
            print("no ")


    # master program loop will run until page limit is reached
    # or the url frontier is empty
    def run(self, N):
        self.findRobotRules()
        i = 0
        while self.urlFront.isEmpty() == False:
            if i < N:
                url = self.urlFront.get()
                print("curr URL: {}".format(url))
                self.spider.crawl(url)
                i+=1
                print("i", i)
                sleep(self.crawlDelay)
            else:
                print("hit page limit {}".format(N))
                return
        print("ran out of URLs to hit")


    # add url to test data links cache
    def reportTestData(self, url):
        self.testDataLinks.append(url)


    # add url to the master node's url frontier
    def addToFront(self, url):
        self.testDataLinks.append(url)
        self.urlFront.put(url)


    # add broken link to broken links cache
    def reportBroken(self, url):
        self.brokenLinks.append(url)


    # add image file to image files cache
    def reportImage(self, url):
        self.imageFiles.append(url)


    # add outgoing link to outgoing links cache
    def reportOutgoing(self, url):
        self.outgoingLinks.append(url)


    # add duplicate link to duplicate links cache
    def reportDuplicate(self, url):
        self.duplicateLinks.append(url)


# print out results report for crawler upon completion of execution
def outputResults(master):
    def prettyPrint(list_, name="list"):
        print("\n[{}]".format(name.upper()))
        for _ in list_:
            if type(list_) == list:
                print("{}".format(_))
            elif type(list_) == dict:
                print("{}[{}]:{}".format(list_,_,list_[_]))
        print("\n")

    prettyPrint(master.brokenLinks, "broken links")
    prettyPrint(master.imageFiles, "image files")
    prettyPrint(master.outgoingLinks, "outgoing links")
    prettyPrint(master.duplicateLinks, "duplicate links")
    prettyPrint(master.pageArchive.archive, "page archive")
    prettyPrint(master.indexer.getNMostFrequent(20, "df"), "20 most frequent (document frequency)")


# load stop words from file
def loadStopWords(path):
    try:
        stopWords = []
        with open(path, encoding='utf-8') as f:
            for line in f.read().splitlines():
                stopWords.append(line)
        f.close()
        return stopWords
    except:
        print("unable to open stopwords file")
        return None


# init function for running crawler program
def main(args):
    if len(args) != 3:
        print("incorrect arguments. exiting...")
        return 1
    N = int(args[1])
    stopWordsFile = args[2]
    stopWords = loadStopWords(stopWordsFile)
    seedSet = ["https://lyle.smu.edu/~fmoore/"]
    master = MasterNode(seedSet, stopWords)
    master.run(N)
    outputResults(master)
    return 0


if __name__ == "__main__":
    exit(main(sys.argv))
    