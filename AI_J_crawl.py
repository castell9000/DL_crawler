import sys
import pandas
import re
import requests
from bs4 import BeautifulSoup

# Created by prtscn@donga.ac.kr / Baek Ji HWan
# 하단의 코드는 깃허브와 구글을 참조하여 만들어졌습니다.
# 코드의 목적은 Artificial intelligence의 논문들을 간편하게 모을 수 있도록 만들어진
# 웹 크롤러 입니다.
# 실행 예시 $ python AI_J_crawl.py
# 사용 환경은 Python 3.7, BeautifulSoup4, pip 18.0, requests 라이브러리를 이용해 만들었습니다.

basicUrl = "https://www.sciencedirect.com/journal/artificial-intelligence/vol"
input = 0
rs_data = []
check = ""
paperUrl = [] #paperSearch() -> redirectPaper() 로 넘겨주는 변수 전역화

def redirectPaper(re_url): #해당 논문으로 이동후 크롤링
    data = [0 for _ in range(9)]  # data 변수 생성 및 형태 잡기

    for r_u in re_url:
        print(r_u +"    test") # #paperSearch() -> redirectPaper() 파라메터 전달 확인
        req2 = requests.get(r_u, headers={'User-Agent': ScholarConf.USER_AGENT})
        html2 = req2.text
        soup2 = BeautifulSoup(html2, 'html.parser')
        re_var1 = soup2.find("article") # 크롤링 라이브러리 태그 범위 설정 변수
        # abs_var = soup2.find(id="abstracts")
        # print(abs_var)
        re_var2 = re_var1.find(class_="Head")
        # print(re_var2)
        re_var3 = re_var1.find(id="aep-abstract-sec-id4")
        re_var4 = re_var1.find(id="author_group")
        re_var5 = re_var1.find(id="aep-keywords-id5")


        if re_var3 == None:
            abs_t = None
        else:
            print(re_var3.get_text())
            abs_t = re_var3.get_text()

        if re_var4 == None:
            filter_aut = "None"
        else:
            aut = re_var4.find_all('a')
            for fa in aut:
                filter_aut = fa.get_text()
        if re_var5 == None :
            filter_key = "None"
        else:
            key_b = re_var5.find_all(class_= "keyword")
            for kb in key_b :
                filter_key = kb.get_text()

        # 데이터 저장
        data[0] = re_var2.get_text()
        data[1] = abs_t
        data[2] = r_u
        data[3] = filter_aut
        data[4] = filter_key
        data[5] = 0 #date
        data[6] = 0 #volume
        data[7] = 0 #issue
        data[8] = 0 #page
        # print(data) # 테스트
        global rs_data # 결과 데이터 변수 전역화
        rs_data.append(data[:]) # data 배열을 슬라이스 하지 않으면 반복문을 빠져나올때 마지막 결과로 모든 배열이 채워짐
        print('', sep="\n")
    print(rs_data)


def paperSearch(): #개별 논문 url 확인
    z=0
    fArray = []
    for x in range(1,2):
        exp= 171+x
        for y in range(0,19):
            iN = y +1
            ex_url = basicUrl+"/"+str(exp)+"/issue/"+str(iN)
            fArray.append(ex_url)
    print(fArray)
    print("aaaaa")
    for pList in fArray :
        req = requests.get(pList, headers={'User-Agent': ScholarConf.USER_AGENT})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find(id="article-list")
        global check
        print("check")
        if article == check:
            print("pass")
            pass
        check = article
        z= z+1
        print("check2")
        print(x)
        a_url = article.find_all("a")
        # print(a_url)
        for p_url in a_url:
            x_url = p_url.get('href')
            if x_url[-4:] == ".pdf":
                pass
            else :
                print(x_url)
                global paperUrl
                paperUrl.append("https://www.sciencedirect.com"+x_url)

    redirectPaper(paperUrl)

# def url(input):
#     if input == 0 :
#         url_in = basicUrl+"?sortOrder=newestFirst&facet-content-type=Article&facet-journal-id=10994"
#         paperSearch(url_in)
#     else:
#         url_in = basicUrl+"?facet-content-type=Article&facet-journal-id=10994&sortOrder=newestFirst&date-facet-mode=between&facet-start-year="+input+"&previous-start-year=1986&facet-end-year="+input2+"&previous-end-year=2018"



class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'


paperSearch() # 프로그램 스타트

# header = ['Title', 'Abstract', 'Paper url', 'Author', 'Keyword', 'Publish_date', 'Volume', 'Issue', 'Pages'] #csv 헤더
# pd = pandas.DataFrame(rs_data) # pandas 라이브러리로 csv 저장
# pd.to_csv("test.csv", encoding="utf-8", header=header)
