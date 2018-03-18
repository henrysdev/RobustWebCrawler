# Henry Warren 2018
# hwarren@smu.edu

from hashlib import md5

class PageArchive():
    def __init__(self):
        self.archive = {}

    def isDuplContent(self, content):
        m = md5()
        m.update(content.encode('utf-8'))
        m = m.hexdigest()
        if m in self.archive:
            return True
        else:
            return False

    def genMd5(self, content):
        m = md5()
        m.update(content.encode('utf-8'))
        return m.hexdigest()

    def addPage(self, url, content):
        hashkey = self.genMd5(content)
        self.archive[hashkey] = url