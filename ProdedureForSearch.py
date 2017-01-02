The steps to execute search.py
>>>import search
>>>crawler=search1.crawler('new.db')
>>> crawler.createindextables()
>>> crawler.crawl()
give it some time to index some pages after some time press Ctrl+C to manually abort the operation
>>>e=search1.searcher('new.db')
>>> e.query('//any word or sentence you want to search type within the quotes')
For second time and other time executions you can directly use:
>>>import search
>>>e=search1.searcher('new.db')
>>> e.query('//any word or sentence you want to search type within the quotes')
