# Henry Warren 2018
# hwarren@smu.edu

from hashlib import md5

class PageArchive():
    def __init__(self):
        self.archive = {}

    def isDuplContent(self, content):
        m = md5()
        m.update(content.encode('utf-8'))
        if m in self.archive:
            return True
        else:
            return False

    def addPage(self, content):
        m = md5()
        m.update(content.encode('utf-8'))
        self.archive[m] = content