import os

from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key=os.environ.get('NEWSAPI_KEY'))

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(
                                          category='business',
                                          language='en', country='us'
                                          )

articles = top_headlines['articles']

for article in articles:
    print(article["url"])