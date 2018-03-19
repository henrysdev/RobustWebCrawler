# Henry Warren 2018
# hwarren@smu.edu

from bs4 import BeautifulSoup
import re


class Tokenizer():
    def __init__(self, stopWords):
        self.stopWords = stopWords


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
        if token in self.stopWords:
            return False
        else:
            return True


    # given a list of text fragments, break into individual words,
    # normalize via tokenization and remove stop words.
    def processText(self, texts):
        texts = list(filter(self.contentVet, texts))
        texts = self.cleanContent(texts)
        # join all text fragments together in order to parse as one long string
        content = ' '.join(texts)
        # find all words in text string and store them in a words list
        words = re.compile(r'[A-z][^.?!\s]*[A-z\d]\b').findall(content)
        # cast all words in words list to lowercase, then filter out the stop words
        tokens = filter(self.isStopword,(map(lambda x: x.lower(),words)))
        return list(tokens)
