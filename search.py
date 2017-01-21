import urllib.request
from bs4 import *
from urllib.parse import urlparse
#from sqlite3 import dbapi2 as sqlite3
import sqlite3
import re
from nltk.corpus import stopwords

ignorewords=set(stopwords.words('english'))

class crawler:
    
    # Initialize the crawler with the name of database
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)
        
    def __del__(self):
        self.con.close()
        
    def dbcommit(self):
        self.con.commit()
        
    # Auxilliary function for getting an entry id and adding
    # it if it's not present
    def getentryid(self,table,field,value,createnew=True):
        c=self.con.cursor()
        cur=c.execute(
        "select rowid from %s where %s='%s'" %(table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=c.execute(
                "insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0]
        
    # Index an individual page
    def addtoindex(self,url,soup):
        #print('Indexing %s' %url)
        if self.isindexed(url):
            return
        print('Indexing '+url)
        
        #get individual words
        text=self.gettextonly(soup)
        words=self.separatewords(text)
        
        #get the url id of the words
        
        urlid=self.getentryid('urllist','url',url)
        
        for i in range(len(words)):
            word=words[i]
            if word in ignorewords:
                continue
            wordid=self.getentryid('wordlist','word',word)
            c=self.con.cursor()
            c.execute("INSERT INTO wordlocation(urlid,wordid,location) VALUES (%d,%d,%d)" %(urlid,wordid,i))
            
    # Extract the text from an HTML page (no tags)
    def gettextonly(self,soup):
        v=soup.string
        if v==None:
            c=soup.contents
            resulttext=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttext+=subtext+'\n'

            return resulttext
        else:
            return v.strip()
        
    # Separate the words by any non-whitespace character
    def separatewords(self,text):
        splitter=re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']
    # Return true if this url is already indexed
    def isindexed(self,url):
        c=self.con.cursor()
        u=c.execute(
            "select rowid from urllist where url='%s'" %url).fetchone()
        if u!=None:
            #check if it has actually been crawled
            v=c.execute(
                'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v!=None:
                return True
            return False
        
    # Add a link between two pages
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass
    
    # Starting with a list of pages, do a breadth
    # first search to the given depth, indexing pages
    # as we go
    
    #def crawl loops through the list of pages , calling addtoindex on each one, it uses beautifulsoup to get all the links 
    def crawl(self,depth=2):
        pages=['http://brickset.com/sets/year-2016'] #This is the list which will store the links to all the pages
        
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=urllib.request.urlopen(page)
                except:
                    print("could not open %s" %page)
                    continue
                    
                #read the contents of the HTML using lxml parser
                soup=BeautifulSoup(c.read(), "lxml")
                #soup=BeautifulSoup(c.read())
                self.addtoindex(page,soup)

                links=soup('a')
                
                #a loop to get the url's from the parent website
                for link in links:
                    if('href' in dict(link.attrs)):
                        url=urllib.parse.urljoin(page,link['href'])
                        if url.find("'")!=-1 :
                            continue
                        url=url.split('#')[0]
                        if url[0:4]=='http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)

                self.dbcommit()

            pages=newpages
       
        
    # Create the database tables, just SQL stuff
    def createindextables(self):
        c=self.con.cursor()
        c.execute('CREATE TABLE urllist(url)')
        c.execute('CREATE TABLE wordlist(word)')
        c.execute('CREATE TABLE wordlocation(urlid,wordid,location)')
        c.execute('CREATE TABLE link(fromid integer,toid integer)')
        c.execute('CREATE TABLE linkwords(wordid,linkid)')
        c.execute('CREATE INDEX wordidx on wordlist(word)')
        c.execute('CREATE INDEX urlidx on urllist(url)')
        c.execute('CREATE INDEX wordurlidx on wordlocation(wordid)')
        c.execute('CREATE INDEX urltoidx on link(toid)')
        c.execute('CREATE INDEX urlfromidx on link(fromid)')
        self.dbcommit()

#a class which let's you do search queries, more of SQL stuff      
class searcher:
    
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self,q):
        #strings to build the query
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]
        c=self.con.cursor()
        # Split the words by spaces
        words=q.split(' ')
        tablenumber=0
        
        for word in words:
            # Get the word ID
            wordrow=c.execute(
                "select rowid from wordlist where word='%s'" % word).fetchone( )
            if wordrow!=None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1
        # Create the query from the separate parts
        fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
        cur=c.execute(fullquery)
        rows=[row for row in cur]
        return rows,wordids

    def getscoredlist(self,rows,wordids):

        totalscores=dict([(row[0],0) for row in rows])

        #this is where we will put the scoring fucntion

        weights=[(1.0,self.frequencyscore(rows))]

        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]
        return totalscores

    def geturlname(self,id):
        c=self.con.cursor()
        return c.execute(
            "select url from urllist where rowid=%d" %id).fetchone()[0]

    def query(self,q):
        rows,wordids=self.getmatchrows(q)
        scores=self.getscoredlist(rows,wordids)
        rankedscores=sorted([(score,url) for (url,score) in scores.items()],reverse=1)
        for (score,urlid) in rankedscores[0:10]:
            print('%f \t %s' %(score,self.geturlname(urlid)))

    #just math to give a score for a webpage from 0 to 1 based on the frequency of words in it
    def normalizescores(self,scores,smallIsBetter=0):
        vsmall=0.00001 #avoid div by 0 err
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0:
                  maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items( )])
        
    def frequencyscore(self,rows):
        counts=dict([(row[0],0) for row in rows])
        for row in rows:
            counts[row[0]]+=1
        return self.normalizescores(counts)

