import selenium
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

def crawling_data(search_url_list):
    
    #크롬드라이버 열기
    driver = wd.Chrome('C:/Users/USER/Desktop/cp1/chromedriver.exe')
    driver.maximize_window()
    
    
    datas = []
    #공고페이지별 data 가져오기
    for i in search_url_list:
        driver.get(i)
        time.sleep(0.5)#멈춰주지 않으면 크롤링할때 오류생김(페이지 가져오는데 시간걸려서 기다려줘야함)

        #예외상황1:근무위치정보 없는경우 
        try:
            근무위치 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[5]/td[3]').text
        except:
            근무위치 = ""    

        #기간정보를 채용시작일과 마감일로 구분
        #예외상황2:기간정보가 상시채용인 경우 오류나기 때문에 try-except활용
        try:
            채용시작일 = re.sub(r'[^0-9:\- ]', '', driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text.split('부터')[0].strip())
            채용마감일 = re.sub(r'[^0-9:\- ]', '', driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text.split('부터')[1].strip())
        except:
            채용시작일 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text.split('부터')[0]
            채용마감일 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text.split('부터')[0]

        #예외상황3:연봉이 페이지에 포함될 경우 인덱스 순서가 망가지기 때문에 try-except활용
        if "만원" in 채용시작일:
            try:
                채용시작일 = re.sub(r'[^0-9:\- ]', '', driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[5]/td[3]').text.split('부터')[0].strip())
                채용마감일 = re.sub(r'[^0-9:\- ]', '', driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[5]/td[3]').text.split('부터')[1].strip())
            except:
                채용시작일 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[5]/td[3]').text.split('부터')[0]
                채용마감일 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[5]/td[3]').text.split('부터')[0]

            근무위치 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[6]/td[3]').text

        기업 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/header/div[1]/h4[1]').text
        직무 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[1]/td[3]').text
        경력 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[3]/td[3]').text
        고용형태 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[2]/td[3]').text


        #예외상황4:고용형태가 없을경우 오류 발생(고용형태 내용이 경력에 들어감)
        if not ('정규' in 고용형태) | ('계약' in 고용형태 ):
            경력 =  driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[2]/td[3]').text
            try:
                채용시작일 = re.sub(r'[^0-9:\- ]', '', driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[3]/td[3]').text.split('부터')[0].strip())
                채용마감일 = re.sub(r'[^0-9:\- ]', '', driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[3]/td[3]').text.split('부터')[1].strip())
            except:
                채용시작일 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[3]/td[3]').text.split('부터')[0]
                채용마감일 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[3]/td[3]').text.split('부터')[0]
            근무위치 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text

            if "만원" in 채용시작일:
                try:
                    채용시작일 = re.sub(r'[^0-9:\- ]', '', driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text.split('부터')[0].strip())
                    채용마감일 = re.sub(r'[^0-9:\- ]', '', driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text.split('부터')[1].strip())
                except:
                    채용시작일 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text.split('부터')[0]
                    채용마감일 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[4]/td[3]').text.split('부터')[0]
                근무위치 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[1]/table/tbody/tr[5]/td[3]').text
            고용형태 = ""




        #예외상황5:기술스택이 포함되어있지 않는 경우 오류 발생 try except 활용
        try:
            업무소개 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[3]/div/div/div').text
            자격조건 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[4]/div/div/div').text

            #예외상황6:우대사항에 타이틀이 아예없는 경우 오류가 발생하므로 try-except 구문 활용
            try:
                우대사항 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[5]/div/div/div/ul[1]').text
            except:
                #예외상황7:우대사항이 아예없는 경우 오류 발생 try-except 활용
                try:
                    우대사항 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[5]/div/div/div').text    
                except:
                    우대사항 = ""

            data = {"채용시작일": 채용시작일,
                    "채용마감일": 채용마감일,
                    "기업": 기업,
                    "직무": 직무,
                    "근무위치": 근무위치,
                    "경력": 경력,
                    "고용형태": 고용형태,
                    "업무소개": 업무소개,
                    "자격조건": 자격조건,
                    "우대사항": 우대사항
                   }

            datas.append(data)
            time.sleep(1.5)#해당 페이지 트래픽 과부하를 방지하여 멈춤시간 갖음

        except:
            업무소개 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[2]/div/div/div').text
            #예외상황8:자격조건,우대사항이 없는 경우 오류 발생 try-except 활용 
            try:
                자격조건 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[3/div/div/div').text

                try:
                    우대사항 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[4]/div/div/div/ul[1]').text
                except:
                    우대사항 = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div/div[1]/section[4]/div/div/div').text    

                data = {"채용시작일": 채용시작일,
                        "채용마감일": 채용마감일,
                        "기업": 기업,
                        "직무": 직무,
                        "근무위치": 근무위치,
                        "경력": 경력,
                        "고용형태": 고용형태,
                        "업무소개": 업무소개,
                        "자격조건": 자격조건,
                        "우대사항": 우대사항
                       }

                datas.append(data)
                time.sleep(1.5)#해당 페이지 트래픽 과부하를 방지하여 멈춤시간 갖음


            except:

                data = {"채용시작일": 채용시작일,
                    "채용마감일": 채용마감일,
                    "기업": 기업,
                    "직무": 직무,
                    "근무위치": 근무위치,
                    "경력": 경력,
                    "고용형태": 고용형태,
                    "업무소개": 업무소개,
                    "자격조건": "",
                    "우대사항": ""
                   }

                datas.append(data)
                time.sleep(1.5)#해당 페이지 트래픽 과부하를 방지하여 멈춤시간 갖음

    datas_df = pd.DataFrame(datas)
    datas_df = datas_df[['채용시작일','채용마감일','기업','직무','근무위치','경력','고용형태','업무소개','자격조건','우대사항']]
    return datas_df