import sys
import pandas
import re
import requests
from bs4 import BeautifulSoup

# Created by prtscn@donga.ac.kr / Baek Ji HWan
# 하단의 코드는 깃허브와 구글을 참조하여 만들어졌습니다.
# 코드의 목적은 Journal of Machine Learning Research의 논문들을 간편하게 모을 수 있도록 만들어진
# 웹 크롤러 입니다.
# basic url의 논문의 볼륨별로 크롤링 하게 만들어졌습니다.
# 실행 명령어 예)python JofML_rs_crwal.py 8
#                -> 볼륨 8의 논문을 크롤링
# 주의! 볼륨 19만 크롤링됨
# 사용 환경은 Python 3.7, BeautifulSoup4, pip 18.0, requests 라이브러리를 이용해 만들었습니다.

basicUrl = "http://jmlr.org"
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
        re_var1 = soup2.find(id="content") # 크롤링 라이브러리 태그 범위 설정 변수
        re_var2 = soup2.find_all('a')
        contentText = re_var1.get_text()

        s1Text = contentText.split('\n\n')
        s2Text = s1Text[0].split('\n')
        print(s2Text)
        s3Text = s2Text[2].split(';')
        s4Text = s3Text[1].split(', ')


        title = s2Text[1]
        abs = s1Text[1]
        author = s3Text[0]
        date = s4Text[1].replace(".","")
        page_b = s4Text[0].replace(" ","").split(':')
        page = page_b[1]
        volume_b = page_b[0].split('(')
        volume = volume_b[0]
        number = volume_b[1].replace(')','')
        pdf = r_u

        # 데이터 저장
        data[0] = title
        data[1] = abs
        data[2] = pdf
        data[3] = author
        data[4] = "none"
        data[5] = date
        data[6] = volume
        data[7] = number
        data[8] = page
        # print(data) # 테스트
        global rs_data # 결과 데이터 변수 전역화
        rs_data.append(data[:]) # data 배열을 슬라이스 하지 않으면 반복문을 빠져나올때 마지막 결과로 모든 배열이 채워짐
        print('', sep="\n")
    print(rs_data)

def paperSearch(url): #개별 논문 url 확인
    req = requests.get(url, headers={'User-Agent': ScholarConf.USER_AGENT})
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    article = soup.find(id="content")
    a_url = article.find_all("a")
    for p_url in a_url:
        checkPurl = p_url.get('href')
        if checkPurl[-5:] == '.html' :
            re_parse = checkPurl
        else:
            continue

        global paperUrl
        if re_parse[0] == "/":
            paperUrl.append(basicUrl+re_parse)
        else :
            paperUrl.append(re_parse)
        print(re_parse)
    redirectPaper(paperUrl)

def url(input): #journal of machine leanring research 볼륨별 목록
    url_in = basicUrl+"/papers/v"+input
    paperSearch(url_in)


class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'


input = sys.argv[1]
url(input) # 프로그램 스타트

header = ['Title', 'Abstract', 'Paper url', 'Author', 'Keyword', 'Publish_date', 'Volume', 'Number', 'Pages'] #csv 헤더
pd = pandas.DataFrame(rs_data) # pandas 라이브러리로 csv 저장
pd.to_csv("test.csv", encoding="utf-8", header=header)
