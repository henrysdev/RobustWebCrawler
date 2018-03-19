# Henry Warren 2018
# hwarren@smu.edu

from urllib.request import urlopen

class Spider():
    def __init__(self, master, parser):
        self.master = master
        self.parser = parser


    # open webpage url and return html source
    def webpageToHtml(self, url):
        try:
            page = urlopen(url).read()
        except:
            print('failed to open URL: {}'.format(url))
            self.master.reportBroken(url)
            return None
        return page


    # obtain html source and pass to parser
    def crawl(self, url):
        content = self.webpageToHtml(url)
        if content is not None:
            self.parser.parse(content, url)