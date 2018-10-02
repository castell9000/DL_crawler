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
gAut = []

def redirectPaper(re_url, author): #해당 논문으로 이동후 크롤링
    data = [0 for _ in range(9)]  # data 변수 생성 및 형태 잡기
    count = 0
    print(len(re_url))
    print(len(author))
    for r_u in re_url:
        fk = ""
        print(r_u +"    test") # #paperSearch() -> redirectPaper() 파라메터 전달 확인
        req2 = requests.get(r_u, headers={'User-Agent': ScholarConf.USER_AGENT})
        html2 = req2.text
        soup2 = BeautifulSoup(html2, 'html.parser')
        re_var1 = soup2.find("article") # 크롤링 라이브러리 태그 범위 설정 변수
        re_var2 = re_var1.find(class_="Head")
        # re_var3 = re_var1.find(id="aep-abstract-sec-id4") #~v198
        re_var3 = re_var1.find(id="as0010") # v199~
        re_var4 = re_var1.find(class_="AuthorGroups")
        re_var5 = re_var1.find(class_="Keywords")
        re_var6 = re_var1.find(class_="text-xs")

        # if re_var3 == None: # 2008 - 2013 v198
        #     for x in range(5,19) :
        #         re_var3 = re_var1.find(id="aep-abstract-sec-id"+str(x))
        #         if re_var3 is not None:
        #             break


        if re_var3 == None:
            abs_t = "None"
        else:
            abs_t = re_var3.get_text()

        if re_var5 == None :
            fk = "None"
            filter_key = fk
        else:
            key_b = re_var5.find_all(class_= "keyword")
            for kb in key_b :
                fk = fk +", "+ kb.get_text()
            filter_key = fk[2:]


        filter_tit = re_var2.get_text()
        aut = re_var4.find_all('a')
        print(aut)
        if aut == []:
            filter_aut = "None"
            print(str(count)+" aa")
        else:
            filter_aut = author[count]
            count = count + 1
            print(filter_aut)
            print(str(count) + " cc")

        pub = re_var6.get_text()
        pub_b = pub.split(",")
        result = []
        for i in pub_b:
            xyz = re.findall('\d+', i)
            result.append(xyz)

        if len(result[0]) < 2:
            volume = result[0]
        else:
            volume = str(result[0][0]) +"-"+str(result[0][1])

        issue = "None"
        date = result[1]
        if result[2] == []: #~v176 배열길이 4 v177~ 배열길이 3
            page = "None"
        else:
            if len(result[2]) <2:
                page = str(result[2])
            else:
                page = str(result[2][0]) + "-" + str(result[2][1])

        # 데이터 저장
        if filter_tit == "Editorial Board":
            continue
        data[0] = filter_tit
        data[1] = abs_t
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


def paperSearch(): #개별 논문 url 확인
    z=0
    fArray = []
    # for x in range(1,6): # 2008~2011
    #     exp= 171+x
    #     for y in range(0,19):
    #         iN = y +1
    #         ex_url = basicUrl+"/"+str(exp)+"/issue/"+str(iN)
    #         fArray.append(ex_url)

    # for x in range(1,23): # 2012 ~ 2013v198
    #     exp= 176+x
    #     ex_url = basicUrl+"/"+str(exp)+"/suppl/C"
    #     fArray.append(ex_url)

    for x in range(1,67): # 2013v199 ~ 2018v264
        exp= 198+x
        ex_url = basicUrl+"/"+str(exp)+"/suppl/C"
        fArray.append(ex_url)
    print(fArray)
    aasd = 0
    for pList in fArray :
        req = requests.get(pList, headers={'User-Agent': ScholarConf.USER_AGENT})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find(id="article-list")

        print("check2")
        a_url = article.find_all("a")
        aut = article.find_all(class_="text-s u-clr-grey8 js-article__item__authors")

        global check
        print("check")
        if article == check:
            print("pass")
            continue
        check = article

        for aa in aut :
            a_aut = aa.get_text()
            if aa == None:
                a_aut = None
                print("None")
            global gAut
            aasd= aasd+1
            print(aasd)
            gAut.append(a_aut)



        check1 = ""
        for p_url in a_url:
            x_url = p_url.get('href')
            if x_url[-4:] == ".pdf":
                pass
            else :
                if check1 == x_url:
                    pass
                else:
                    print(x_url)
                    check1 = x_url
                    global paperUrl
                    paperUrl.append("https://www.sciencedirect.com"+x_url)
    print(gAut)
    print(paperUrl)
    redirectPaper(paperUrl, gAut)



class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'


paperSearch() # 프로그램 스타트

header = ['Title', 'Abstract', 'Paper url', 'Author', 'Keyword', 'Publish_date', 'Volume', 'Issue', 'Pages'] #csv 헤더
pd = pandas.DataFrame(rs_data) # pandas 라이브러리로 csv 저장
pd.to_csv("test.csv", encoding="utf-8", header=header)
