from bs4 import BeautifulSoup #HTML문서를 피싱하기 위한 라이브러리
import requests #HTTP 요청을 보내기 위한 라이브러리
import pandas as pd #데이터 처리르 위한 라이브러리
import datetime #날짜 /시간 처리르 위한 라이브러리
import re #정규 표현식을 사용하기 위한 라이브러리

category = ['politics', 'Economic', 'social', 'culture', 'world', 'IT']  #네이버 뉴스의 6개 주요 색션

url = 'https://news.naver.com/section/100' #카테고리 1번째 URL

df_titles = pd.DataFrame()             # 모든 색션의 뉴스 제목을 저장할 데이터 프레임

for i in range(6):
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

df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(   #전체 데이터프레임에 현재 색션 데이터 추가
        datetime.datetime.now().strftime('%Y%m%d')), index=False)

