# Henry Warren 2018
# hwarren@smu.edu

from bs4 import BeautifulSoup
import re


STOPWORDS = ["a","about","an","and","are","as", 
             "at","be","by","com","for","from", 
             "how","i","in","is","it","of","on", 
             "or","that","the","this","to","was", 
             "what","when","where","who","will", 
             "with","then","www"]


class Tokenizer():
    def __init__(self, stopwords=STOPWORDS):
        self.stopwords = stopwords


    # filter function for determining if text contains newline element
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


    # filter function for determining if token is a stopword
    def isStopword(self, token):
        if token in self.stopwords:
            return False
        else:
            return True


    # given a list of text fragments, break into individual words,
    # normalize via tokenization and remove stopwords.
    def processText(self, texts):
        texts = list(filter(self.contentVet, texts))
        texts = self.cleanContent(texts)
        content = ' '.join(texts)
        words = re.compile(r'[A-z][^.?!\s]*[A-z\d]\b').findall(content)
        tokens = filter(self.isStopword,(map(lambda x: x.lower(),words)))
        return list(tokens)
