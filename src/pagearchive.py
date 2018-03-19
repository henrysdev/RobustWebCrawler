# Henry Warren 2018
# hwarren@smu.edu

from hashlib import md5

class PageArchive():
    def __init__(self):
        self.archive = {}


    # generate md5 hash and return digest
    def genMd5(self, content):
        m = md5()
        m.update(content.encode('utf-8'))
        return m.hexdigest()


    # take hash of content and compare to archive to
    # determine if an exact duplicate exists
    def isDuplContent(self, content):
        contentHash = self.genMd5(content)
        if contentHash in self.archive:
            return True
        else:
            return False


    # add a new entry of the format {hashkey:url} to archive
    def addPage(self, url, content):
        hashkey = self.genMd5(content)
        self.archive[hashkey] = url