# Henry Warren 2018
# hwarren@smu.edu

from bs4 import BeautifulSoup

class Parser():
    def __init__(self, master, urlfilter, pagearchive):
        self.master = master
        self.urlfilter = urlfilter
        self.pagearchive = pagearchive

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
            #texts[i] = texts[i].replace(' ','')
        return texts

    def parse(self, page):
        soup = BeautifulSoup(page, 'lxml')
        soup.prettify()
        texts = soup.findAll(text=True)
        texts = list(filter(self.contentVet, texts))
        texts = self.cleanContent(texts)
        content = ' '.join(texts)
        # return if content is whitespace
        if content is None or content =='' or content.isspace():
            return
        # return if content is duplicate
        if self.pagearchive.isDuplContent(content):
            return
        # archive new content
        else:
            self.pagearchive.addPage(content)
        self.extractUrls(soup)
