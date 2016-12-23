from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

class LinkParser(HTMLParser):

    def handle_starttag(self,tag, attrs):
        if tag=='a'

        for (key,value) in attrs:
            if key=='href':
                newUrl=parse.urljoin(self.baseUrl,value)
                self.links=self.links+[newUrl]

    def getLinks(self,url):
        self.links=[]
        self.baseUrl=url
        response=urlopen(url)
        if response.getheader('Content-Type')=='text/html':
            htmlBytes=response.read()
            htmlString=htmlBytes.decode("utfj-8")
            self.feed(htmlString)
            return htmlString,self.links
        else:
            return "",[]

def spider(url,word,maxPages):
    gesToVisit=[url]
    numberVisited=0
    foundWord=False
    while numberVisited<maxPages and pagesToVisit !=[] and not foundWord:
        numberVisited=numberVisited+1
        urll=pagesToVisit[0]
        pagesToVisit=pagesToVisit[1:]
        try:
            print('visiting')
            parser=LinkParser()
            data,links=parser.getLinks(url)
            if data.find(word)>-1
                foundWord=True
            PagesToVisit=pagesToVisit+links
            print('success')
        except:
            print('failed')
