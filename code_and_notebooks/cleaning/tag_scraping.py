from bs4 import BeautifulSoup
from urllib.request import urlopen

def make_links():
    list_of_links = []
    for i in range(1,1419):
         list_of_links.append('http://stackoverflow.com/tags?page={}&tab=popular'.format(i))
    return list_of_links

def scrap(links):
    tags = []
    for i in links:
        html = urlopen(i)
        bs = BeautifulSoup(html,'lxml')
        for i in bs.findAll(name='a', attrs={'class':'post-tag'}):
            tags.append(i.text)
    return tags
