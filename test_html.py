import sys
import pandas
import re
import requests
from bs4 import BeautifulSoup

def test() :
    req2 = requests.get("https://www.sciencedirect.com/search?qs=machine%20learning&pub=Expert%20Systems%20with%20Applications&cid=271506&show=25&sortBy=relevance&years=2009&offset=250", headers={'User-Agent': ScholarConf.USER_AGENT})
    html2 = req2.text
    soup2 = BeautifulSoup(html2, 'html.parser')
    re_var1 = soup2.select("ol.search-result-wrapper")  # 크롤링 라이브러리 태그 범위 설정 변수

    # re_var4 = re_var1.find(class_="text-xs")

    print(re_var1)
    # aut = re_var4.get_text()
    # test = aut.split(",")
    # result =[]
    # print(test)
    # for i in test:
    #     cc=re.findall('\d+', i)
    #     result.append(cc)
    # print(result)
    # print(len(result[3]))

class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'

off = []
offsets = 169//25
for of in range(1,offsets+1):
    set = of * 25
    off.append(str(set))
print(off)
test()