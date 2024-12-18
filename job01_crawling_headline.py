from bs4 import BeautifulSoup
import requests
import pandas as pd
import datetime
import re

category = ['politics', 'Economic', 'social', 'culture', 'world', 'IT']

url = 'https://news.naver.com/section/100'

#url = 'https://news.naver.com/section/100'
 #     'https://news.naver.com/section/101'
  #    'https://news.naver.com/section/102'
   #   'https://news.naver.com/section/103'
    #  'https://news.naver.com/section/105'
     # 'https://news.naver.com/section/104'

df_titles = pd.DataFrame()

for i in range(6):
    url = 'https://news.naver.com/section/10{}'.format(i)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    title_tags = soup.select('.sa_text_strong')
    titles = []
    for title_tag in title_tags:
        title = title_tag.text
        title = re.compile('[^가-힣 ]').sub('',title)
        titles.append(title)
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows', ignore_index=True)
print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
        datetime.datetime.now().strftime('%Y%m%d')), index=False)

