#from requests import options
from selenium import webdriver      #웹 브라우저 자동화를 위한 기본 라이브러리
from selenium.webdriver.common.by import By #요소 찾기를 위한 방법 지정
from selenium.webdriver.chrome.service import Service as ChromeService  #크롬 서비스 관리
from selenium.webdriver.chrome.options import  Options as ChromeOptions #크롬 옵션설정
from webdriver_manager.chrome import ChromeDriverManager    #크롬 드라이버 자동 관리
from selenium.common.exceptions import  NoSuchElementException  #요소를 찾지 못할 때의 예외
from selenium.common.exceptions import StaleElementReferenceException   #요소가 변경됐을 때의 예외
import pandas as pd      #데이터 처리
import re   #정규 표현식
import time #시간 지연
import datetime #날짜/시간 처리
from bs4 import BeautifulSoup
import requests

options = ChromeOptions()   #크롬 옵션 객체 생성
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'  #사용자 에이전트 설정(브라우저 식별)
options.add_argument('user_agent=' + user_agent)
#사용자 에이전트 설정이유:
#정상적인라우저로 인식, 웹사이트 차단 우회,웹  스크래핑 방지


options.add_argument('lang=ko_KR')

service = ChromeService(executable_path=ChromeDriverManager().install())    #크롬 드라이버 서비스 설정
driver = webdriver.Chrome(service=service, options=options)                 #크롬 드라이버 생성

url='https://news.naver.com/section/100'

driver.get(url)
button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
time.sleep(1)
for i in range(10):
    time.sleep(0.5)
    driver.find_element(By.XPATH, button_xpath).click()

for i in range(1,98):
    for j in range(1,7):
        title_xpath = '//*[@id="newsct"]/div[4]/div/div[1]/div[{}]/ul/li[{}]/div/div/div[2]/a/strong'.format(i,j)
        try:
            title= driver.find_element(By.XPATH, title_xpath).text
            print(title)
        except:
            print(i,j)

category = ['politics', 'Economic', 'social', 'culture', 'world', 'IT']  #네이버 뉴스의 6개 주요 색션


df_titles = pd.DataFrame()             # 모든 색션의 뉴스 제목을 저장할 데이터 프레임

for i in range(0,1):
    url = 'https://news.naver.com/section/10{}'.format(i)     # 각 색션별 URL 생성
    resp = requests.get(url)                                   #HTTP Get 요청으로 웹 페이지 가져오기
    soup = BeautifulSoup(resp.text, 'html.parser')      #BeautifulSoup 객체 생성하여 HTML 피싱
    title_tags = soup.select('.sa_text_strong')                 #css선택자를 사용하여 뉴스 제목 태그 선택
                                                                #sa_text_strong 클래스를 가진 모든 요소 선택
    titles = []             #제목 추출 및 전처리
    for title_tag in title_tags:
        title = title_tag.text      #태그에서 텍스트 추출
        title = re.compile('[^가-힣 ]').sub('',title)     #정규식을 사용하여 한글과 공백만 남기고 모두 제거
        titles.append(title)                                  #[^가-힣]: 한글과 공백이 아닌 문자

    df_section_titles = pd.DataFrame(titles, columns=['titles'])    #현재 섹션의 제목들을 데이터프레임으로 변환
    df_section_titles['category'] = category[i]     #카테고리 정보 추가
    df_titles = pd.concat([df_titles, df_section_titles],   #전체 데이터프레임에 현재 섹션 데이터 추가
                          axis='rows',  #행 방향으로 연결
                          ignore_index=True)   #인덱스 재설정
print(df_titles.head()) #상위 5개 행 출력하여 데이터 확인

df_titles.info()    #데이터프레임 정보 출력(데이터 타입, 결측치 등)

print(df_titles['category'].value_counts())     #카테고리별 기사 수 확인

df_titles.to_csv('./crawling_data/naver_headline_news_politics.csv'.format(   #전체 데이터프레임에 현재 색션 데이터 추가
        datetime.datetime.now().strftime('%Y%m%d')), index=False)
time.sleep(30)
driver.close()

