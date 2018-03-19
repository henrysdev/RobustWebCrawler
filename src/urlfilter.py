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


    # add a restricted path (found from robots.txt)
    def addRestrictedPath(self, path):
        self.restrictedPaths.append(path)
        print("restricted paths: {}".format(self.restrictedPaths))


    # determine if passed url has been found already
    def isDuplicate(self, url):
        if url not in self.foundUrls:
            return False
        else:
            return True

    # determine if passed url is path to an image file
    def isImageFile(self, url):
        for ftype in self.imgTypes:
            if url.endswith(ftype) or url.endswith(ftype.upper()):
                return True
        return False


    # determine if passed url is in a restricted path
    def isRestrictedUrl(self, url):
        for fdir in self.restrictedPaths:
            if fdir in url:
                return True
        return False


    # add url to url frontier
    def addUrl(self, url):
        timestamp = time.time()
        self.foundUrls[url] = timestamp
        self.master.addToFront(url)


    # filter found urls and add eligible links to the url frontier
    def vetUrl(self, url):
        for baseUrl in self.seedSet:
            tmpUrl = url
            # if href link is a relative link, make it an absolute link
            if tmpUrl[:4] != "http":
                tmpUrl = "{}{}".format(baseUrl, tmpUrl)
            # throw away link if disallowed access (adhering to robots.txt)
            if self.isRestrictedUrl(tmpUrl):
                return
            # continue only if url is within the domain we are scraping
            if tmpUrl.startswith(baseUrl) or baseUrl[5:] in tmpUrl:
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
                self.master.reportOutgoing(tmpUrl)
