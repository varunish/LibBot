from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
from PyPDF2 import PdfFileReader
from io import StringIO

class LinkParser(HTMLParser):

    def handle_starttag(self,tag, attrs):
        if tag=='a':
            for (key,value) in attrs:
                if key=='href':
                    newUrl=parse.urljoin(self.baseUrl,value)
                    self.links=self.links+[newUrl]
    
    def get_pdf_text(self, response):
        """ Peek inside PDF to check possible violations."""

        

        

        stream = StringIO.StringIO(response.body)
        reader = PdfFileReader(stream)

        text = ""

        

        for page in reader.pages:
                # XXX: Does handle unicode properly?
                text += page.extractText()

        return text

    def getLinks(self,url):
        self.links=[]
        self.baseUrl=url
        response=urlopen(url)
        ct = response.headers.get("content-type", "").lower()
        if "pdf" in ct:
                # Assume a PDF file
                data = self.get_pdf_text(response)
        else:
                # Assume it's HTML
                data = response.body
        #if response.getheader('Content-Type')=='text/html':
            #htmlBytes=response.read()
            #htmlString=htmlBytes.decode("utfj-8")
            #self.feed(htmlString)
                return data,self.links

def spider(url,word,maxPages):
    pagesToVisit=[url]
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
            if data.find(word)>-1:
                foundWord=True
            pagesToVisit=pagesToVisit+links
            print('success')
        except:
            print('failed')

spider("www.google.com","web",100)
