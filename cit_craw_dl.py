import sys
import csv
import json
import pandas
import requests
from bs4 import BeautifulSoup

# Created by prtscn@donga.ac.kr / Baek Ji HWan
# 하단의 코드는 깃허브와 구글을 참조하여 만들어졌습니다.
# 코드의 목적은 Journal of Machine Learning의 논문들을 간편하게 모을 수 있도록 만들어진
# 웹 크롤러 입니다.
# 사용 환경은 Python 3.7, BeautifulSoup4, pip 18.0, requests 라이브러리를 이용해 만들었습니다.


rs_data = []

paperUrl = [] #paperSearch() -> redirectPaper() 로 넘겨주는 변수 전역화

def redirectPaper(re_url): #해당 논문으로 이동후 크롤링
    data = [0 for _ in range(9)]  # data 변수 생성 및 형태 잡기
    count = 0
    for r_u in re_url:
        print(r_u +"    test") # #paperSearch() -> redirectPaper() 파라메터 전달 확인
        req2 = requests.get(r_u, headers={'User-Agent': ScholarConf.USER_AGENT})
        html2 = req2.text
        soup2 = BeautifulSoup(html2, 'html.parser')
        re_var1 = soup2.find(class_="ArticleHeader main-context") # 크롤링 라이브러리 태그 범위 설정 변수
        re_var2 = soup2.find(class_="Abstract")
        re_var3 = soup2.find(class_="test-contributor-names")
        re_var4 = soup2.find(class_="KeywordGroup")
        re_var5 = soup2.find(class_="icon--meta-keyline-before")

        if re_var2 == None :
            data[1]="This paper not exist abstract"
        else:
            data[1] = re_var2.find(id="Par1").get_text() #abstract 처리

        collect_author = re_var3.find_all(class_="authors__name")
        filter_aut = []
        for x in collect_author:
            filter_aut.append(x.get_text().replace('\xa0', " ")) #저자 이름 불순물 필터링

        filter_key=[]
        if re_var4 == None :
            filter_key = "This paper not exist keyword"
        else:
            collect_keyword = re_var4.find_all(class_="Keyword")
            for x in collect_keyword:
                filter_key.append(x.get_text().replace('\xa0', "")) # 키워드 처리

        data[0] = re_var1.find(class_="ArticleTitle").get_text()
        data[2] = r_u
        data[3] = filter_aut
        data[4] = filter_key
        data[5] = re_var5.find('time').get('datetime')
        data[6] = re_var5.find(class_="ArticleCitation_Volume").get_text().replace(",","")
        data[7] = re_var5.find(class_="ArticleCitation_Issue").get_text().replace("\xa0","")
        data[8] = re_var5.find(class_="ArticleCitation_Pages").get_text()
        print(data)
        global rs_data
        rs_data.append(data[:])
        print('', sep="\n")
    print(rs_data)

    #
    # print(rs_data)

def paperSearch(url): #개별 논문 url 확인
    req = requests.get(url, headers={'User-Agent': ScholarConf.USER_AGENT})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find(id="results-list")
    a_url = article.find_all(class_="title")
    # print(a_url)
    # print(soup)
    for p_url in a_url:
        re_parse = p_url.get('href')

        global paperUrl
        paperUrl.append("https://link.springer.com/"+re_parse)

    redirectPaper(paperUrl)

def url(): #journal of machine leanring 목록
    url_in = "https://link.springer.com/search?sortOrder=newestFirst&facet-content-type=Article&facet-journal-id=10994"
    paperSearch(url_in)

class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'


url() # 프로그램 스타트
header = ['Title', 'Abstract', 'Paper url', 'Author', 'Keyword', 'Publish_date', 'Volume', 'Issue', 'Pages']
pd = pandas.DataFrame(rs_data)
pd.to_csv("test.csv", encoding="utf-8", header=header)
