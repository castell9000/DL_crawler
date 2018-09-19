import sys
import csv
import json
import requests
from bs4 import BeautifulSoup

# req = requests.get(url)

data = ' '

data= {
            'title':           None,
            'url':             None,
            'author':          None,
            'publisher':       None,
        }

def set_url(url):
    req = requests.get(url, headers={'User-Agent': ScholarConf.USER_AGENT})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find(id="gsc_a_b")
    papers = table.findAll(class_="gsc_a_tr")
    # print(soup)
    for paper in papers:
        web = paper.find("a")
        web2 = paper.find_all('div')
        link = web.get('data-href')
        data['title'] = web.get_text()
        data['url'] = 'https://scholar.google.co.kr/' + link
        data['author'] = web2[0].get_text()
        data['publisher'] = web2[1].get_text()
        print(data)
        # print('Title : ' + title, sep='\n')
        # print('Paper Link : ' + url2, sep='\n')
        # print('Author : ' + web2[0].get_text(), sep='\n')
        # print('Publisher : ' + web2[1].get_text(), sep='\n')

        print('', sep="\n")

def url(keyword):
    url_in = "https://scholar.google.co.kr/citations?user="+keyword+"&hl=en"
    print(url_in)
    set_url(url_in)

class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'

keyword = sys.argv[1]
print(keyword)
url(keyword)

#
# f = csv.writer(open("test.csv", "w", encoding='utf-8'))
#
# # Write CSV Header, If you dont need that, remove this line
# f.writerow(["title", "url", "author", "publisher"])
#
# for x in data:
#     f.writerow(["title"], ["url"], ["author"], ["publisher"])