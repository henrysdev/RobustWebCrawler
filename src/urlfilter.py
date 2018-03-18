# Henry Warren 2018
# hwarren@smu.edu

import time

FRESHOLD = 5000000
IMG_TYPES = ['.png','.jpg','.gif','.jpeg']

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

    def isImageFile(self, url):
        for _ in IMG_TYPES:
            if url.endswith(_) or url.endswith(_.upper()):
                return True
        return False

    def addUrl(self, url):
        timestamp = time.time()
        self.foundUrls[url] = timestamp
        self.master.addToFront(url)

    def vetUrl(self, url):
        for baseUrl in self.seedSet:
            tmpUrl = url
            if tmpUrl[:4] != "http":
                tmpUrl = "{}{}".format(baseUrl, tmpUrl)
            if tmpUrl.startswith(baseUrl):
                if self.isImageFile(tmpUrl):
                    self.master.reportImage(tmpUrl)
                    return
                if self.isDuplicate(tmpUrl) == False:
                    self.addUrl(tmpUrl)
                else:
                    lastTime = self.foundUrls[tmpUrl]
                    #print("last time crawled: {}".format(lastTime))
                    if abs(time.time() - lastTime) > FRESHOLD: # check for freshness
                        self.addUrl(tmpUrl)
