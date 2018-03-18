# Henry Warren 2018
# hwarren@smu.edu

from bs4 import BeautifulSoup
from time import sleep
import sys
from queue import *

from spider import Spider
from parser import Parser
from urlfilter import UrlFilter
from pagearchive import PageArchive
from indexer import Indexer


# queue for holding found urls to be crawled
class UrlFrontier():
    def __init__(self, seedSet):
        self.urlQueue = Queue()
        for url in seedSet:
            self.urlQueue.put(url)
        print(self.urlQueue)


    def put(self, url):
        self.urlQueue.put(url)


    def get(self):
        return self.urlQueue.get()


    def isEmpty(self):
        return self.urlQueue.empty()


# managing object for controlling data flow in the crawler 
class MasterNode():
    def __init__(self, seedSet):
        self.seedSet = seedSet
        self.urlFront = UrlFrontier(seedSet)
        self.pageArchive = PageArchive()
        self.urlFilter = UrlFilter(self)
        self.indexer = Indexer(self)
        self.parser = Parser(self, 
                             self.urlFilter, 
                             self.pageArchive,
                             self.indexer)
        self.spider = Spider(self, self.parser)
        self.brokenLinks = []
        self.imageFiles = []
        self.outgoingLinks = []


    def run(self, N):
        i = 0
        while self.urlFront.isEmpty() == False:
            if i < N:
                url = self.urlFront.get()
                print("curr URL: {}".format(url))
                self.spider.crawl(url)
                i+=1
                print("i", i)
                sleep(2)
            else:
                return


    def addToFront(self, url):
        self.urlFront.put(url)


    def reportBroken(self, url):
        self.brokenLinks.append(url)


    def reportImage(self, url):
        self.imageFiles.append(url)


    def reportOutgoing(self, url):
        self.outgoingLinks.append(url)


def outputResults(master):
    print("broken links: {}".format(master.brokenLinks))
    print("image files: {}".format(master.imageFiles))
    print("outgoing links: {}".format(master.outgoingLinks))
    print("page archive: {}".format(master.pageArchive.archive))
    print("most frequent 20 words (tf): {}".format(master.indexer.getNMostFrequent(20,"tf")))
    print("most frequent 20 words (df): {}".format(master.indexer.getNMostFrequent(20,"df")))


def main(args):
    if len(args) != 2:
        print("incorrect arguments. exiting...")
    N = int(args[1])
    seedset = ["https://s2.smu.edu/~fmoore/"]
    master = MasterNode(seedset)
    master.run(N)
    outputResults(master)


if __name__ == "__main__":
    main(sys.argv)
    