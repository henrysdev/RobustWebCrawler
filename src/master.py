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
    def __init__(self, seedSet):
        self.seedSet = seedSet
        self.urlFront = UrlFrontier(seedSet)
        self.pageArchive = PageArchive()
        self.urlFilter = UrlFilter(self)
        self.indexer = Indexer()
        self.parser = Parser(self, 
                             self.urlFilter, 
                             self.pageArchive,
                             self.indexer)
        self.spider = Spider(self, self.parser)
        self.testDataLinks = []
        self.brokenLinks = []
        self.imageFiles = []
        self.outgoingLinks = []


    # master program loop will run until page limit is reached
    # or the url frontier is empty
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


# print out results report for crawler upon completion of execution
def outputResults(master):
    def prettyPrint(list_, name="list"):
        print("[{}]\n".format(name.upper()))
        for _ in list_:
            if type(list_) == list:
                print("{}".format(_))
            elif type(list_) == dict:
                print("{}[{}]:{}".format(list_,_,list_[_]))

    prettyPrint(master.brokenLinks, "broken links")
    prettyPrint(master.imageFiles, "image files")
    prettyPrint(master.outgoingLinks, "outgoing links")
    prettyPrint(master.pageArchive.archive, "page archive")
    prettyPrint(master.indexer.getNMostFrequent(20, "df"), "20 most frequent (document frequency)")


# init function for running crawler program
def main(args):
    if len(args) != 2:
        print("incorrect arguments. exiting...")
        return 1
    N = int(args[1])
    seedset = ["https://s2.smu.edu/~fmoore/"]
    master = MasterNode(seedset)
    master.run(N)
    outputResults(master)
    return 0


if __name__ == "__main__":
    exit(main(sys.argv))
    