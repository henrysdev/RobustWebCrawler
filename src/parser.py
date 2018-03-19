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


    # extract urls from html source by 'href' attribute of 'a' tag
    def extractUrls(self, soup):
        for a in soup.find_all('a', href=True):
            #print("Found the URL: {}".format(a['href']))
            foundUrl = a['href']
            self.urlfilter.vetUrl(foundUrl)


    # filter function for removing all newline elements in source text
    def contentVet(self, element):
        if "\n" in element:
            return False
        else:
            return True


    # function for cleaning up pre-filtered text terms
    def cleanContent(self, texts):
        for i in range(len(texts)):
            texts[i] = texts[i].replace('\n',' ')
            texts[i] = texts[i].replace('\r',' ')
        return texts


    # determines if found page type is required to be indexed
    def isIndexablePage(self, url):
        for t in self.indexable_types:
            if t in url or t.upper() in url:
                return True
        return False


    # normalize tokens for the purpose of equivalence classes
    # via splitting into delimited words and casting to lower case
    def tokenize(self, content):
        low = lambda x: x.lower()
        words = re.compile(r'[A-z][^.?!\s]*[A-z\d]\b').findall(content)
        tokens = list(map(low,words))
        return tokens


    # inspect and extract elements from html source such as
    # links to other pages and text to be indexed
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
                tokens = self.tokenize(content)
                self.indexer.indexDoc(tokens, url)
