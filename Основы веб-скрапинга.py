import requests
from bs4 import BeautifulSoup
import pandas as pd

def parse_habr(queries,number_page):
  result = []
  BASE_URL = 'https://habr.com'
  pages = [1]
  if (number_page > 1):
    pages = range (1,number_page)
  for q in queries:
     df = pd.DataFrame()
     for i in pages:
        resp = requests.get(BASE_URL + f'/ru/search/page{i}/', params={
                          'q': q,
                          'target_type': 'posts',
                          'order': 'relevance'})
        soup = BeautifulSoup(resp.text)
        for article_tag in soup.find_all('article'):
            
            date = pd.to_datetime(soup.find('time')).get('datetime')
            title = article_tag.find('h2').get_text()
            link = BASE_URL+title.find('a').get('href')
            full_text = soup.find('div', class_='article-formatted-body').text.strip()
            rating = article_tag.find('span', class_='tm-votes-meter__value').get_text()
            row = {'date': date, 'title': title, 'link': link,'full_text': full_text, 'rating': rating }
            df = pd.concat([df, pd.DataFrame([row])])
     result.append(df)       
  return result

result = parse_habr (['pandas','анализ данных'], 3)
print(result)