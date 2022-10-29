import file_save
import time, re, datetime, json, random

from bs4 import BeautifulSoup # pip install beautifulsoup4, pip install lxml
from selenium import webdriver # pip install selenium, 추가로 버전에 맞는 chromedriver.exe 받아서 같은 폴더로 이동필요
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # pip install ChromeDriverManager

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = True
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def purifyText(text):
    ''' 특수문자 제거한 문자를 반환한다. '''
    result = re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", text)
    return result

def dateFormat(dateText): 
    '''
    2022.10.28 12:11 -> 22/10/28 12:11과 같이 맞춘다.
    "5 분 전", "5 시간 전"과 같은 값이 들어온 경우 현재 시간 기준으로 고려한다.
    '''
    if "전" in dateText:
        current = datetime.datetime.now()
        
        a, b, _ = dateText.split() # ex. 5 시간 전 -> a: 5, b: 시간
        a = int(a)
        if b == "시간":
            target = current - datetime.timedelta(hours=a-1) # 61분 전이 2시간 전으로 표기되기에 a-1처리
        elif b == "분":
            target = current - datetime.timedelta(minutes=a)
        else:
            target = current
        
        return target.strftime("%y/%m/%d %H:%M")
    else:
        return dateText.replace(".", "/")[2:]

visited = None
visitedFileNameRef = None
browser = None

def init(visitedFileName):
    global visited, browser, visitedFileNameRef
    
    if visitedFileNameRef == visitedFileName:
        return
    
    visited = set(file_save.fileToArray(visitedFileName)) # 이미 방문한 글 번호 저장
    visitedFileNameRef = visitedFileName

    browser = set_chrome_driver()
    browser.maximize_window()

def crawling(visitedFileName = "fmkorea_visited_post.txt", page = 5):
    '''     
    커뮤니티에서 한페이지의 글과 댓글목록을 읽고, 글 번호 저장 파일을 갱신하고 json배열을 리턴
        Args:
            visitedFileName: 방문한 글 번호들이 저장된 파일명
            page: 몇 번째 페이지를 조회할 것인지
        
        Returns:
            글과 댓글에 대응하는 json파일 20개가 배열에 담겨 return
    '''
    global visited, browser
    
    init(visitedFileName)
    newVisited = set() # 새로 방문한 글 번호 저장
    result = []
    timeSleep = 3 # 몇 초 간격으로 조회할건지 (너무 짧게하면 차단위험)

    # https://www.fmkorea.com/index.php?mid=humor&page=XXX 로 접속
    url = "https://www.fmkorea.com/index.php?mid=humor&page={}".format(page)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "lxml")

    
    ############################
    ##### 각 페이지별 처리 #####
    ############################
    
    # <td class="title hotdeal_var8"> 안에 있는 <a href="/123512...">에 접근
    tdList = soup.find_all("td", attrs={"class": "hotdeal_var8"})
    for td in tdList: # 한 페이지에서 20개의 글 제목을 확인할 수 있으며 이 각각이 td
        postNum = td.a["href"] # 글 번호
        if postNum in visited or postNum in newVisited: # 이미 방문한 건 패스
            continue
        else:
            newVisited.add(postNum)
        postUrl = "https://www.fmkorea.com" + postNum # 각 글에 대한 링크
        
        # 각 페이지에서의 각각의 글 조회
        browser.get(postUrl)
        soupSub = BeautifulSoup(browser.page_source, "lxml")
        
        ############################
        ##### 각 글에 대한 처리 #####
        ############################
        
        # post["date"]의 경우 22/10/18 15:04와 같은 형식을 맞춘다.
        post = {"board": "유머/움짤/이슈", "title": None, "content": None, "username": None, "date": None, "comments": []}
        if not soupSub.find("div", attrs={"class": "top_area"}): # 게시글이 삭제되었을 경우 처리
            print("삭제된 게시글 확인")
            continue
        
        post["title"] = purifyText(soupSub.find("h1", attrs={"class": "np_18px"}).get_text())
        post["content"] = purifyText(soupSub.find("div", attrs={"class": "xe_content"}).get_text())
        post["username"] = purifyText(soupSub.find("a", attrs={"class": "nick"}).get_text())
        # 글 날짜의 경우 2022.10.28 12:11 -> 22/10/28 12:11과 같이 맞춘다.
        post["date"] = dateFormat(soupSub.find("span", attrs={"class": "date"}).get_text())
        
        
        ## 댓글이 있을 경우처리
        if soupSub.find("ul", attrs={"class": "fdb_lst_ul"}):
            commentList = soupSub.find("ul", attrs={"class": "fdb_lst_ul"}).find_all("li")
            for comm in commentList:
                comment = {"username": None, "message": None, "time": None}
                
                comment["username"] = purifyText(comm.find("a").get_text())
                comment["message"] = purifyText(comm.find("div", attrs={"class": "xe_content"}).get_text())
                comment["time"] = dateFormat(comm.find("span", attrs={"class": "date"}).get_text())
                
                post["comments"].append(comment)
        
        print("글 제목:", post["title"])
        result.append(post)
        time.sleep(random.uniform(timeSleep - 0.5, timeSleep + 0.5))
    print(result)   
        
    # 방문목록과 파일 갱신해주고, newVisited -> visited로 이동
    file_save.arrayToFile(visitedFileName, list(newVisited))
    visited.update(newVisited)

    # JSON배열 결과 리턴
    return result