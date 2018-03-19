# Henry Warren 2018
# hwarren@smu.edu

from bs4 import BeautifulSoup

import indexer
from tokenizer import Tokenizer

class Parser():
    def __init__(self, master, urlfilter, pagearchive, indexer):
        self.master = master
        self.urlfilter = urlfilter
        self.pagearchive = pagearchive
        self.indexer = indexer
        self.tokenizer = Tokenizer()
        self.indexable_types = ['.txt','.htm','.html','.php']


    # extract urls from html source by 'href' attribute of 'a' tag
    def extractUrls(self, soup):
        for a in soup.find_all('a', href=True):
            foundUrl = a['href']
            self.urlfilter.vetUrl(foundUrl)


    # determines if found page type is required to be indexed
    def isIndexablePage(self, url):
        for t in self.indexable_types:
            if t in url or t.upper() in url:
                return True
        return False


    # parse robots.txt file for rules
    def extractRules(self, soup):
        texts = soup.findAll(text=True)
        content = ' '.join(texts)
        rules = []
        for line in content.splitlines():
            if line[0] == "#":
                continue
            kvPair = line.split(':')
            rules.append((kvPair[0],kvPair[1]))
        self.master.setCrawlRules(rules)


    # inspect and extract elements from html source such as
    # links to other pages and text to be indexed
    def parse(self, pageHtml, url, robots=False):
        soup = BeautifulSoup(pageHtml, 'lxml')
        soup.prettify()
        if robots == True:
            self.extractRules(soup)
            return
        self.extractUrls(soup)
        if self.isIndexablePage(url):
            texts = soup.findAll(text=True)
            tokens = self.tokenizer.processText(texts)
            content = ' '.join(tokens)
            # return if content is whitespace
            if content is None or content =='' or content.isspace():
                return
            # return if content is duplicate
            if self.pagearchive.isDuplContent(content):
                self.master.reportDuplicate(url)
                return
            # archive new content + split into words for indexing
            else:
                self.pagearchive.addPage(url, content)
                # split content into words and index document
                self.indexer.indexDoc(tokens, url)
