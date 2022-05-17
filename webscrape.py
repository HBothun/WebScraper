import urllib.request as url
from bs4 import BeautifulSoup

def stateWikiScan(stateWikiUrl, numberOfRows):

    ##########SATE ROW SIZE CHART##########
    # Minnesota = 62
    # WisConsin = 69
    # Illinois = 73
    # North Dakota = 70
    # South Dakota = 75
    # Iowa = 57 #

    html = url.urlopen(stateWikiUrl)
    soup = BeautifulSoup(html, 'html.parser')

    print(soup.title.string)
    first = soup.find('tr', class_='mergedtoprow ib-settlement-official')
    data1 = first.getText()
    print(data1)
    i = 0
    while i <= numberOfRows:
        if i == 0:
            newInfo = first.find_next('tr', class_='mergedtoprow')
        else:
            newInfo = newInfo.find_next('tr')
        newData = newInfo.getText()
        print(newData)
        i += 1

stateWikiScan('https://en.wikipedia.org/wiki/Minnesota', 62)