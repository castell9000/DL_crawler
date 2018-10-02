import sys
import pandas
import re
import requests
from bs4 import BeautifulSoup

def test() :
    req2 = requests.get("https://www.sciencedirect.com/science/article/pii/S0004370211001305", headers={'User-Agent': ScholarConf.USER_AGENT})
    html2 = req2.text
    soup2 = BeautifulSoup(html2, 'html.parser')
    re_var1 = soup2.find("article")  # 크롤링 라이브러리 태그 범위 설정 변수

    re_var4 = re_var1.find(class_="text-xs")

    print(re_var4)
    aut = re_var4.get_text()
    test = aut.split(",")
    result =[]
    print(test)
    for i in test:
        cc=re.findall('\d+', i)
        result.append(cc)
    print(result)
    print(len(result[3]))

class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'

test()