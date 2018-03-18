# Henry Warren 2018
# hwarren@smu.edu

from bs4 import BeautifulSoup
import re

import indexer

class Parser():
    def __init__(self, master, urlfilter, pagearchive, indexer):
        self.master = master
        self.urlfilter = urlfilter
        self.pagearchive = pagearchive
        self.indexer = indexer
        self.indexable_types = ['.txt','.htm','.html','.php']


    def extractUrls(self, soup):
        for a in soup.find_all('a', href=True):
            #print("Found the URL: {}".format(a['href']))
            foundUrl = a['href']
            self.urlfilter.vetUrl(foundUrl)


    def contentVet(self, element):
        if "\n" in element:
            return False
        else:
            return True


    def cleanContent(self, texts):
        for i in range(len(texts)):
            texts[i] = texts[i].replace('\n',' ')
            texts[i] = texts[i].replace('\r',' ')
        return texts


    def isIndexablePage(self, url):
        for t in self.indexable_types:
            if t in url or t.upper() in url:
                return True
        return False


    def parse(self, pageHtml, url):
        soup = BeautifulSoup(pageHtml, 'lxml')
        soup.prettify()
        self.extractUrls(soup)
        if self.isIndexablePage(url):
            texts = soup.findAll(text=True)
            texts = list(filter(self.contentVet, texts))
            texts = self.cleanContent(texts)

            content = ' '.join(texts)
            # return if content is whitespace
            if content is None or content =='' or content.isspace():
                return
            # return if content is duplicate
            if self.pagearchive.isDuplContent(content):
                print("DUPLICATE FOUND AT: {}".format(url))
                return
            # archive new content + split into words for indexing
            else:
                self.pagearchive.addPage(url, content)
                # split content into words and index document
                low = lambda x: x.lower()
                words = re.compile(r'[A-z][^.?!\s]*[A-z\d]\b').findall(content)
                words = list(map(low,words))
                self.indexer.indexDoc(words, url)
