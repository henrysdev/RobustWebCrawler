# Henry Warren 2018
# hwarren@smu.edu

import urllib.request

class Spider():
    def __init__(self, master, parser, userAgent="*"):
        self.master = master
        self.parser = parser
        self.userAgent = userAgent


    # proper member method for setting UA
    def setUserAgent(self, userAgent):
        self.userAgent = userAgent


    # open webpage url and return html source
    def webpageToHtml(self, url):
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': self.userAgent
            }
        )
        try:
            page = urllib.request.urlopen(req).read()
        except:
            print('failed to open URL: {}'.format(url))
            self.master.reportBroken(url)
            return None
        return page


    # obtain html source and pass to parser
    def crawl(self, url, rtnHtml=False):
        content = self.webpageToHtml(url)
        if content is not None:
            if rtnHtml:
                self.parser.parse(content, url, robots=True)
            else:
                self.parser.parse(content, url)