# Henry Warren 2018
# hwarren@smu.edu

from bs4 import BeautifulSoup
from time import sleep
import sys
from spider import Spider
from parser import Parser
from urlfilter import UrlFilter
from queue import *


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

    def __str__(self):
        rtnStr = ""
        for elem in list(self.urlQueue):
            rtnStr += str(elem)
        return rtnStr


class MasterNode():
    def __init__(self, seedSet):
        self.seedSet = seedSet
        self.urlFront = UrlFrontier(seedSet)
        self.urlfilter = UrlFilter(self)
        self.parser = Parser(master=self, urlfilter=self.urlfilter)
        self.spider = Spider(master=self, parser=self.parser)
        self.brokenLinks = []
        self.imageFiles = []

    def run(self):
        while self.urlFront.isEmpty() == False:
            url = self.urlFront.get()
            print(url)
            self.spider.crawl(url)
            sleep(2)

    def addToFront(self, url):
        self.urlFront.put(url)

    def reportBroken(self, url):
        self.brokenLinks.append(url)


def init(seedSet):
    master = MasterNode(seedSet)
    master.run()


if __name__ == "__main__":
    SEEDSET = ["https://s2.smu.edu/~fmoore/"]
    init(SEEDSET)