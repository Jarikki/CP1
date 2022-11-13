import selenium
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import csv

#기업별 공고 페이지 url 가져오기
def search_url():
    
    #크롬드라이버 열기
    driver = wd.Chrome('C:/Users/USER/Desktop/cp1/chromedriver.exe')
    driver.maximize_window()

    base_url = 'https://career.programmers.co.kr/job?page=1&order=recent'
    driver.get(base_url)
    time.sleep(1)
    
    #직무 선택버튼
    driver.find_element(By.XPATH,'//*[@id="search-form"]/div[2]/div[1]/button').click()
    time.sleep(1)

    #서버/백엔드, 프론트엔드, 머신러닝, 인공지능(AI), 데이터 엔지니어, DBA 직무 체크
    driver.find_element(By.XPATH,'//*[@id="search-form"]/div[2]/div[1]/div/ul/li[1]/label/input').click()
    time.sleep(0.1)
    driver.find_element(By.XPATH,'//*[@id="search-form"]/div[2]/div[1]/div/ul/li[2]/label/input').click()
    time.sleep(0.1)
    driver.find_element(By.XPATH,'//*[@id="search-form"]/div[2]/div[1]/div/ul/li[6]/label/input').click()
    time.sleep(0.1)
    driver.find_element(By.XPATH,'//*[@id="search-form"]/div[2]/div[1]/div/ul/li[7]/label/input').click()
    time.sleep(0.1)
    driver.find_element(By.XPATH,'//*[@id="search-form"]/div[2]/div[1]/div/ul/li[8]/label/input').click()
    time.sleep(0.1)
    driver.find_element(By.XPATH,'//*[@id="search-form"]/div[2]/div[1]/div/ul/li[9]/label/input').click()
    time.sleep(2)

    #최초페이지 파싱
    page = driver.page_source
    soup = BeautifulSoup(page,'lxml')
    time.sleep(3)

    #페이지 번호 추출
    page_num = []
    a = soup.find_all("span", attrs={"class": "page-link"})
    for i in a:
        page_num.append(re.sub(r"[^0-9]","",i.get_text()))
    page_num = [int(a) for a in page_num if a]

    #기업 공고별 url추출
    page_url_list = []

    #최초페이지 세부 url추출
    page_url_list_temp = [code.get_attribute('href') for i in range(1,21) for code in driver.find_elements(By.CSS_SELECTOR,f"#list-positions-wrapper > ul > li:nth-child({i}) > div.item-body > div.position-title-wrapper > h5 > a")]
    page_url_list = page_url_list + page_url_list_temp

    #페이지 이동 및 세부페이지 url추출(첫 5페이지)
    for j in range(3,7):
        driver.find_element(By.XPATH,f'//*[@id="tab_position"]/div[3]/ul/li[{j}]/span').click()
        time.sleep(1)

        #페이지 공고별 코드추출
        page_url_list_temp = [code.get_attribute('href') for i in range(1,21) for code in driver.find_elements(By.CSS_SELECTOR,f"#list-positions-wrapper > ul > li:nth-child({i}) > div.item-body > div.position-title-wrapper > h5 > a")]
        page_url_list = page_url_list + page_url_list_temp

    #페이지 이동 및 세부페이지 url추출(6페이지~ (마지막-3)페이지)
    rep = 6
    while rep <= (page_num[-1] - 3):
        driver.find_element(By.XPATH,f'//*[@id="tab_position"]/div[3]/ul/li[7]/span').click()
        time.sleep(1)

        #페이지 공고별 코드추출
        page_url_list_temp = [code.get_attribute('href') for i in range(1,21) for code in driver.find_elements(By.CSS_SELECTOR,f"#list-positions-wrapper > ul > li:nth-child({i}) > div.item-body > div.position-title-wrapper > h5 > a")]
        page_url_list = page_url_list + page_url_list_temp
        rep += 1

    #페이지 이동 및 세부페이지 url추출(마지막 3페이지)
    for j in range(6,9):
        driver.find_element(By.XPATH,f'//*[@id="tab_position"]/div[3]/ul/li[{j}]/span').click()
        time.sleep(1)

        #페이지 공고별 코드추출
        page_url_list_temp = [code.get_attribute('href') for i in range(1,21) for code in driver.find_elements(By.CSS_SELECTOR,f"#list-positions-wrapper > ul > li:nth-child({i}) > div.item-body > div.position-title-wrapper > h5 > a")]
        page_url_list = page_url_list + page_url_list_temp

    
    #스케줄링 사용- 검색할 새로운 url만 추출(이전 사용했던 url을 제외)
    #이전 크롤링 때 사용한 url 불러오기
    try: 
        page_url_list_total = []
        with open('list_to_csv.csv','r',newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                page_url_list_total.extend(row)
    except:
        pass
    
    #이전 사용했던 url 제외 및 업데이트
    try: #첫번째 이후 크롤링
        search_url_list = list(set(page_url_list) - set(page_url_list_total))

    except: #첫 크롤링 
        search_url_list = page_url_list


    #추가된 이전사용한 url 저장 
    with open('list_to_csv.csv','a',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(search_url_list)


    return search_url_list