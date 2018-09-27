import sys
import pandas
import re
import requests
from bs4 import BeautifulSoup

# Created by prtscn@donga.ac.kr / Baek Ji HWan
# 하단의 코드는 깃허브와 구글을 참조하여 만들어졌습니다.
# 코드의 목적은 Journal of Machine Learning의 논문들을 간편하게 모을 수 있도록 만들어진
# 웹 크롤러 입니다.
# 실행 예시 $ python JofML_crawl.py 2008 2018
#             -> 2008년에서 2018년의 모든 게제글 크롤링
# 뒤의 인풋숫자 없이 실행은 가능하나 가장 최근의 20개 게재글만 가져옵니다.
# 사용 환경은 Python 3.7, BeautifulSoup4, pip 18.0, requests 라이브러리를 이용해 만들었습니다.

basicUrl = "https://link.springer.com/search"
input = 0
rs_data = []

paperUrl = [] #paperSearch() -> redirectPaper() 로 넘겨주는 변수 전역화

def redirectPaper(re_url): #해당 논문으로 이동후 크롤링
    data = [0 for _ in range(9)]  # data 변수 생성 및 형태 잡기

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

        # Web 상의 Null 데이터 처리 조건문 시작
        if re_var2 == None :
            abs = "This paper not exist abstract"
        elif re_var2.find(id="Par1") != None:
            abs = re_var2.find(id="Par1").get_text() #abstract 처리
        else:
            abs = re_var2.find(class_="Para").get_text().replace(",", "")

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

        if re_var5.find('time') == None:
            date = "This paper pubilished online only"
        else:
            date = re_var5.find('time').get('datetime') # 발행날짜 처리

        if re_var5.find(class_="ArticleCitation_Volume") == None:
            volume = "No Volume"
        else:
            volume = re_var5.find(class_="ArticleCitation_Volume").get_text().replace(",", "") # 볼륨 처리

        if re_var5.find(class_="ArticleCitation_Issue") == None:
            issue = "No issue"
        else:
            issue = re_var5.find(class_="ArticleCitation_Issue").get_text().replace("\xa0","") # 이슈 처리

        if re_var5.find(class_="ArticleCitation_Pages") == None:
            page = "No page"
        else:
            page = re_var5.find(class_="ArticleCitation_Pages").get_text() # 페이지 처리
        # Web 상의 Null 데이터 처리 조건문 종료

        # 데이터 저장
        data[0] = re_var1.find(class_="ArticleTitle").get_text()
        data[1] = abs
        data[2] = r_u
        data[3] = filter_aut
        data[4] = filter_key
        data[5] = date
        data[6] = volume
        data[7] = issue
        data[8] = page
        # print(data) # 테스트
        global rs_data # 결과 데이터 변수 전역화
        rs_data.append(data[:]) # data 배열을 슬라이스 하지 않으면 반복문을 빠져나올때 마지막 결과로 모든 배열이 채워짐
        print('', sep="\n")
    print(rs_data)

def paperSearch_year(url, input, input2):
    req = requests.get(url, headers={'User-Agent': ScholarConf.USER_AGENT})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    rs_num = soup.find(class_="number-of-search-results-and-search-terms")
    before_num = rs_num.get_text() # 총 결과수 태그 입력값 가져오기
    nu = re.findall("\d+", before_num) # 총 결과수 내의 숫자만 가져오기
    num = int(nu[0]) # int 타입으로 변환
    print(num)
    if num%20 == 0:
        page_num = int(num/20)
    else:
        page_num = int((num/20)+1)

    for i in range(page_num):
        url_p = basicUrl+"/page/"+str(i+1)+"?facet-content-type=Article&facet-journal-id=10994&sortOrder=newestFirst&date-facet-mode=between&facet-start-year="+input+"&previous-start-year=1986&facet-end-year="+input2+"&previous-end-year=2018"
        print(url_p)
        req_page = requests.get(url_p, headers={'User-Agent': ScholarConf.USER_AGENT})
        html_page = req_page.text
        soup_page = BeautifulSoup(html_page, 'html.parser')
        article = soup_page.find(id="results-list")
        a_url = article.find_all(class_="title")
        for p_url in a_url:
            re_parse = p_url.get('href')

            global paperUrl
            paperUrl.append("https://link.springer.com" + re_parse)

    print(paperUrl)
    redirectPaper(paperUrl)

def paperSearch(url): #개별 논문 url 확인
    req = requests.get(url, headers={'User-Agent': ScholarConf.USER_AGENT})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find(id="results-list")
    a_url = article.find_all(class_="title")
    for p_url in a_url:
        re_parse = p_url.get('href')

        global paperUrl
        paperUrl.append("https://link.springer.com"+re_parse)

    redirectPaper(paperUrl)

def url(input): #journal of machine leanring 목록
    if input == 0 :
        url_in = basicUrl+"?sortOrder=newestFirst&facet-content-type=Article&facet-journal-id=10994"
        paperSearch(url_in)
    else:
        url_in = basicUrl+"?facet-content-type=Article&facet-journal-id=10994&sortOrder=newestFirst&date-facet-mode=between&facet-start-year="+input+"&previous-start-year=1986&facet-end-year="+input2+"&previous-end-year=2018"
        paperSearch_year(url_in, input,input2)


class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'


input = sys.argv[1]
input2 = sys.argv[2]

url(input) # 프로그램 스타트

header = ['Title', 'Abstract', 'Paper url', 'Author', 'Keyword', 'Publish_date', 'Volume', 'Issue', 'Pages'] #csv 헤더
pd = pandas.DataFrame(rs_data) # pandas 라이브러리로 csv 저장
pd.to_csv("test.csv", encoding="utf-8", header=header)
