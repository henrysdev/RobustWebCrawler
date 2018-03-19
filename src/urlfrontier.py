# Henry Warren 2018
# hwarren@smu.edu

from queue import *

# queue (FIFO) for holding found urls to be crawled
class UrlFrontier():
    def __init__(self, seedSet):
        self.urlQueue = Queue()
        for url in seedSet:
            self.urlQueue.put(url)


    # add item to (the back of the) queue
    def put(self, url):
        self.urlQueue.put(url)


    # pop and return next item in the queue
    def get(self):
        return self.urlQueue.get()


    # check if queue is empty
    def isEmpty(self):
        return self.urlQueue.empty()