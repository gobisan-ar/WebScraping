import requests
from bs4 import BeautifulSoup

response = requests.get("https://news.ycombinator.com/news")
web_data = response.text

soup = BeautifulSoup(web_data, 'html.parser')

articles = soup.find_all(name="a", class_='titlelink')
article_texts = []
article_links = []

for article in articles:
    text = article.getText()
    article_texts.append(text)
    link = article.get("href")
    article_links.append(link)

article_upvotes = [int(score.getText().split()[0]) for score in soup.find_all(name="span", class_="score")]

max_upvotes = max(article_upvotes)
top_article = article_upvotes.index(max_upvotes)

print("TOP ARTICLE")
print(article_texts[top_article])
print(article_links[top_article])
