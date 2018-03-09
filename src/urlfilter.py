# Henry Warren 2018
# hwarren@smu.edu

import time

FRESHOLD = 5000000

class UrlFilter():
    def __init__(self, master):
        self.master = master
        self.seedSet = master.seedSet
        self.foundUrls = {}

    def isDuplicate(self, url):
        if url not in self.foundUrls:
            return False
        else:
            return True

    def addUrl(self, url):
        timestamp = time.time()
        print(timestamp)
        self.foundUrls[url] = timestamp
        self.master.addToFront(url)

    def vetUrl(self, url):
        print("Filter URL: {}".format(url))
        for baseUrl in self.seedSet:
            if url[:4] != "http":
                url = "{}{}".format(baseUrl, url)
            print(url)
            if url.startswith(baseUrl):
                if self.isDuplicate(url) == False:
                    self.addUrl(url)
                else:
                    lastTime = self.foundUrls[url]
                    print("last time crawled: {}".format(lastTime))
                    if abs(time.time() - lastTime) > FRESHOLD: # check for freshness
                        self.addUrl(url)
