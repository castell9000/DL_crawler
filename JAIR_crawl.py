import sys
import pandas
import re
import requests
from bs4 import BeautifulSoup

# Created by prtscn@donga.ac.kr / Baek Ji HWan
# 하단의 코드는 깃허브와 구글을 참조하여 만들어졌습니다.
# 코드의 목적은 Ja의 논문들을 간편하게 모을 수 있도록 만들어진
# 웹 크롤러 입니다.
# 실행 예시 $ python ES_A_crawl.py
# 사용 환경은 Python 3.7, BeautifulSoup4, pip 18.0, requests 라이브러리를 이용해 만들었습니다.

basicUrl = "https://www.jair.org/index.php/jair/issue/view/"
input = 0
rs_data = []
volume = []
check = ""
paperUrl = [] #paperSearch() -> redirectPaper() 로 넘겨주는 변수 전역화
gAut = []
ck =""
pageArr = []


def redirectPaper(re_url, author, pages, vol): #해당 논문으로 이동후 크롤링
    data = [0 for _ in range(9)]  # data 변수 생성 및 형태 잡기
    count = 0
    print(len(re_url))
    print(len(author))
    ccc = 0
    for r_u in re_url:

        fk = ""
        print(r_u +"    test") # #paperSearch() -> redirectPaper() 파라메터 전달 확인
        req2 = requests.get(r_u, headers={'User-Agent': ScholarConf.USER_AGENT})
        html2 = req2.text
        soup2 = BeautifulSoup(html2, 'html.parser')
        re_var1 = soup2.find(class_="article-details") # 크롤링 라이브러리 태그 범위 설정 변수

        if re_var1 == None:
            print("no paper")
            continue

        re_var2 = re_var1.find(class_="page-header")
        re_var3 = re_var1.find(class_="article-abstract")
        re_var5 = re_var1.find(class_="list-group-item date-published")
        re_var4 = re_var1.find(class_="authors")

        if re_var3 == None:
            abs_t = "None"
        else:
            abs_t = re_var3.get_text()

        filter_tit = re_var2.get_text()
        aut = re_var4.find_all(class_="article-author")

        if aut == []:
            filter_aut = "None"
            print(str(count)+" aa")
        else:
            filter_aut = author[count]
            count = count + 1
            print(filter_aut)
            print(str(count) + " cc")

        filter_date = re_var5.get_text()

        title = filter_tit.replace("\n", "")
        abstract = abs_t.replace("\n", "")
        date = filter_date.replace("Published", "")
        date = date.replace("\n", "")

        title = title.replace("\t", "")
        abstract = abstract.replace("\t", "")
        date = date.replace("\t", "")

        filter_key = "None"
        issue = "None"

        # 데이터 저장
        data[0] = title
        data[1] = abstract
        data[2] = r_u
        data[3] = filter_aut
        data[4] = filter_key
        data[5] = date
        data[6] = vol[ccc]
        data[7] = issue
        data[8] = pages[ccc]
        ccc = ccc+1
        print(data) # 테스트
        global rs_data # 결과 데이터 변수 전역화
        rs_data.append(data[:]) # data 배열을 슬라이스 하지 않으면 반복문을 빠져나올때 마지막 결과로 모든 배열이 채워짐
        print('', sep="\n")
    print(rs_data)


def paperSearch(year): #개별 논문 url 확인

    fArray = []
    bYear = []
    years = int(year) - 2008
    setY = 1115+(years*3)
    setV = 31 + (years*3)

    for of in range(setY, setY+3):
        set = of
        bYear.append(str(set))

    for y in bYear:
        ex_url = basicUrl+y
        fArray.append(ex_url)

    print(fArray)
    aasd = 0
    for pList in fArray :
        req = requests.get(pList, headers={'User-Agent': ScholarConf.USER_AGENT})
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        article = soup.find(class_="section")
        a_url = article.find_all("a")
        aut = article.find_all(class_="authors")
        pg = article.find_all(class_="pages")
        print("check")

        for aa in aut :  # 저자명 배열에 담기 / 문자열 정리
            a_aut = aa.get_text()
            if aa == None:
                a_aut = None
                print("None")
            global gAut
            aasd= aasd+1
            print(aasd)
            print(a_aut)
            a_aut = a_aut.replace("\n", "")
            gAut.append(a_aut.replace("\t", ""))
            global volume
            volume.append(str(setV))

        setV = setV + 1

        for pp in pg :  # 저자명 배열에 담기 / 문자열 정리
            a_pg = pp.get_text()
            if pp == None:
                a_pg = None
                print("None")
            global pageArr
            a_pg = a_pg.replace("\n", "")
            pageArr.append(a_pg.replace("\t", ""))

        for p_url in a_url:
            x_url = p_url.get('href')
            if len(x_url) == 54:
                global paperUrl
                paperUrl.append(x_url)

            else:
                print("This url is not paper abs")
                continue
    print(gAut)
    print(volume)
    print(pageArr)
    print(paperUrl)
    redirectPaper(paperUrl, gAut, pageArr, volume)



class ScholarConf(object):
    USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'


input = sys.argv[1]


paperSearch(input) # 프로그램 스타트

# header = ['Title', 'Abstract', 'Paper url', 'Author', 'Keyword', 'Publish_date', 'Volume', 'Issue', 'Pages'] #csv 헤더
# pd = pandas.DataFrame(rs_data) # pandas 라이브러리로 csv 저장
# pd.to_csv("test.csv", encoding="utf-8", header=header)
