class crawler:
    #initialise the crawler with the name of database
    def _init__(self,dbname):
        pass

    def _def__(self):
        pass

    def dbcommit(self):
        pass

    #auxillary function for getting an entry id and adding
    #it if its not present

    def getentryid(self,table,field,value,createnew=True):
        return None

    #Index an individual page
    def addtoindex(self,url,soup):
        print 'Indexing %s'%url

    #Extract the text from an HTML page(no tags)
    def gettextonly(self,soup):
        return None
    #Separate the words by any non-whitespace character
    def separatewords(self,text):
        return None
    #Return true if this url is already indexed
    def isindexed(self,url):
        return False
    #Add a link between two pages
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass

    #Starting with a list of pages , do a breadth
    #first search to the given depth, indexing pages
    #as we go
    def crawl(self,pages,depth=2):
        pass
    #create the database tables
    def createindextables(self):
        pass
