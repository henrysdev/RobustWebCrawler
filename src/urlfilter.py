# Henry Warren 2018
# hwarren@smu.edu

import time

class UrlFilter():
    def __init__(self, master, freshTime=5000000):
        self.master = master
        self.seedSet = master.seedSet
        self.foundUrls = {}
        self.freshTime = freshTime
        self.imgTypes = ['.png','.jpg','.gif','.jpeg']
        self.restrictedPaths = []


    def addRestrictedPath(self, path):
        self.restrictedPaths.append(path)


    def isDuplicate(self, url):
        if url not in self.foundUrls:
            return False
        else:
            return True


    def isImageFile(self, url):
        for ftype in self.imgTypes:
            if url.endswith(ftype) or url.endswith(ftype.upper()):
                return True
        return False


    def isPdfFile(self, url):
        if url.endswith('.pdf') or url.endswith('.PDF'):
            return True
        else:
            return False


    def isRestrictedUrl(self, url):
        for fdir in self.restrictedPaths:
            if fdir in url:
                return True
        return False


    def addUrl(self, url):
        timestamp = time.time()
        self.foundUrls[url] = timestamp
        self.master.addToFront(url)


    def vetUrl(self, url):
        for baseUrl in self.seedSet:
            tmpUrl = url
            # throw away link if pdf file (cant be parsed as html)
            if self.isPdfFile(url):
                print("pdf files cannot be easily parsed with html")
                return
            # throw away link if disallowed access (adhering to robots.txt)
            if self.isRestrictedUrl(url):
                print("scraping not permmitted at this location")
                return
            # if href link is relative link, change to definite link
            if tmpUrl[:4] != "http":
                tmpUrl = "{}{}".format(baseUrl, tmpUrl)
            # continue only if url is within the domain we are scraping
            if tmpUrl.startswith(baseUrl):
                if self.isImageFile(tmpUrl):
                    self.master.reportImage(tmpUrl)
                    return
                if self.isDuplicate(tmpUrl) == False:
                    self.addUrl(tmpUrl)
                else:
                    lastTime = self.foundUrls[tmpUrl]
                    # check for url freshness if crawled previously
                    if abs(time.time() - lastTime) > self.freshTime:
                        self.addUrl(tmpUrl)
                    else:
                        return
            else:
                master.reportOutgoing(url)
